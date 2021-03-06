import calendar
import json
import os
import os.path
import re
import spacy

from datetime import datetime as dt
from pymetamap import MetaMap

INPUT_FILE = 'medhelp.jl'  # path to the jsonlines scraped data
METAMAP_PATH = '/home/shatru-u/app/public_mm/bin/metamap'
MM_SEMTYPES_MAP = {
    'dsyn': 'diseases',
    'sosy': 'symptoms',
    'topp': 'treatments',
    'clnd': 'drugs',
    'bpoc': 'bodyParts',
}
BATCH_SIZE = 50  # process these many items at once and save
ISO_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
TIMESTAMP_FORMATS = {
    'health24': '%Y/%m/%d%z',
    'medhelp': ISO_FORMAT,
    'patient_info': '%Y-%m-%dT%H:%M%z',
}
FINAL_KEYS_IN_OUTPUT = {
    'id', 'link', 'group', 'author', 'created', 'heading', 'content', 'numReplies',
    'lastActivityTs', 'expertReplies', 'numExpertReplies', 'authorsWeight', 'numWords', 'diseases',
    'symptoms', 'treatments', 'drugs', 'bodyParts', 'site'
}

# Metamap instance
mm = MetaMap.get_instance(METAMAP_PATH)
# Spacy for tokenizing post to sentences
nlp = spacy.load('en_core_web_sm')

# Get the forum for which the input file is
forum = None
for site in TIMESTAMP_FORMATS.keys():
    if site in INPUT_FILE:
        forum = site
        break

# Load authors for the forum
authors = None
in_fname, in_ext = INPUT_FILE.split('.')
authors_fname = in_fname + '_authors.json'
if os.path.isfile(authors_fname):
    with open(authors_fname) as f:
        authors = json.load(f)


def metamap(sentences):
    result = {}
    for semname in MM_SEMTYPES_MAP.values():
        result[semname] = set()

    concepts, error = mm.extract_concepts(sentences,
                                          restrict_to_sts=MM_SEMTYPES_MAP.keys(),
                                          no_derivational_variants=True,
                                          unique_acronym_variants=True)
    if not error:
        for concept in concepts:
            if concept.__class__.__name__ is not 'ConceptAA':
                for semtype, semname in MM_SEMTYPES_MAP.items():
                    if semtype in concept.semtypes:
                        # Sometimes the diseases come as single string with commas
                        for name in concept.preferred_name.lower().split(', '):
                            result[semname].add(name)
    for k in result:
        result[k] = list(result[k])  # convert sets to list
    return result


def get_datetime(ts, format=TIMESTAMP_FORMATS[forum]):
    # Replace the last ':' in timezone -06:00 to avoid error on python 3.6
    return dt.strptime(''.join(ts.rsplit(':', 1)), format)


def get_epoch(ts):
    # ISO_FORMAT since post timestamps have already been fixed to ISO format
    dtm = get_datetime(ts, ISO_FORMAT)
    # calendar.timegm to get seconds from UTC epoch
    # Python sucks for timezones! Appparently timegm doesn't take into account TZ offset!
    return calendar.timegm(dtm.timetuple()) - dtm.tzinfo.utcoffset(dtm).seconds


# Make sure every timestamp is in same format 2019-11-26T20:36:15-06:00
def fix_timestamp(ts):
    return get_datetime(ts).isoformat()


def preprocess_post(post):
    post['site'] = forum

    replies = post.get('replies', [])
    # Extract expert replies and max weight for the authors
    # authorsWeight = Collective weight of authors present in post and replies
    if forum == 'health24':
        # Since all replies on health24 are from an expert
        post['expertReplies'] = replies
        post['numExpertReplies'] = len(post['expertReplies'])
        post['authorsWeight'] = float(min(1, post['numExpertReplies']))

        # Add timezone information so that it can be formatted correctly
        post['created'] = fix_timestamp(post['created'] + '+00:00')
        for r in replies:
            r['created'] = fix_timestamp(r['created'] + '+00:00')
    else:  # We have author info for other 2 websites
        post['created'] = fix_timestamp(post['created'])
        post['expertReplies'] = []
        post['authorsWeight'] = 0.0
        for r in replies:
            if authors[r['author']]['weight'] == 1.0:
                post['expertReplies'].append(r)
            post['authorsWeight'] = max(post['authorsWeight'], authors[r['author']]['weight'])
            r['created'] = fix_timestamp(r['created'])
        post['numExpertReplies'] = len(post['expertReplies'])

    if replies:
        post['lastActivityTs'] = get_epoch(replies[-1]['created'])  # last reply time
    else:
        post['lastActivityTs'] = get_epoch(post['created'])

    post.pop('replies', None)  # Drop replies, only keep expertReplies
    return post


def process_post(post):
    post = preprocess_post(post)

    # heading + content + replies
    totalcontent = post['group'] + ': ' + post['heading'] + '. ' + post['content']
    for reply in post['expertReplies']:
        totalcontent += reply['content']

    # To avoid MetaMap errors
    totalcontent = totalcontent.encode('ascii', errors='ignore').decode()
    post['numWords'] = len(re.findall(r'\w+', totalcontent))  # Count words

    # Do Metamap processing after tokenizing content into sentences
    result = metamap(nlp(totalcontent).sents)
    post.update(result)

    # Restrict keys in the output to a fixed set
    post_keys = list(post.keys())
    for k in post_keys:
        if k not in FINAL_KEYS_IN_OUTPUT:
            post.pop(k, None)

    return post


out_fname = in_fname + '_mm.' + in_ext
with open(out_fname, 'w+') as out_file:
    with open(INPUT_FILE) as in_file:
        num_processed = 0
        processed_posts = []
        for line in in_file:
            print('Processing post %d' % (num_processed + 1))
            post = json.loads(line)
            processed_post = process_post(post)
            num_processed += 1
            # Add an id if not present; for health24
            if 'id' not in processed_post:
                processed_post['id'] = str(num_processed)
            processed_posts.append(json.dumps(processed_post))
            if num_processed % BATCH_SIZE == 0:
                print('Writing batch #%d to file %s' % (num_processed // BATCH_SIZE, out_fname))
                # Dump the batch to disk
                out_file.write('\n'.join(processed_posts))
                out_file.write('\n')
                # https://docs.python.org/2/library/stdtypes.html#file.flush
                out_file.flush()
                os.fsync(out_file)
                # reset batch
                processed_posts = []

        # Write the last batch out
        out_file.write('\n'.join(processed_posts))
