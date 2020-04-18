import json
import os
import re
import time
from datetime import datetime

import spacy
from pymetamap import MetaMap

INPUT_FILE = 'health24.jl'  # path to the jsonlines scraped data
METAMAP_PATH = '/home/shatru-u/app/public_mm/bin/metamap'
MM_SEMTYPES_MAP = {
    'dsyn': 'diseases',
    'sosy': 'symptoms',
    'topp': 'treatments',
    'clnd': 'drugs',
    'bpoc': 'bodyParts',
}
BATCH_SIZE = 5  # process these many items at once and save
TIMESTAMP_FORMATS = {
    'health24': '%Y/%m/%d',
    'medhelp': '%Y-%m-%d %H:%M:%S%z',
    'patient_info': '%Y-%m-%d %H:%M:%S%z',
}

mm = MetaMap.get_instance(METAMAP_PATH)
nlp = spacy.load('en_core_web_sm')

# Get the forum for which the input file is
forum = None
for site in TIMESTAMP_FORMATS.keys():
    if site in INPUT_FILE:
        forum = site
        break


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
                        result[semname].add(concept.preferred_name)
    for k in result:
        result[k] = list(result[k])  # convert sets to list
    return result


def parse_timestamp(string):
    return time.mktime(time.strptime(string, TIMESTAMP_FORMATS[forum]))


def preprocess_post(post):
    if post['replies']:
        post['lastReplyTs'] = parse_timestamp(post['replies'][-1]['created'])

    if forum == 'health24':
        post['expertReplies'] = post['replies']

    return post


def process_post(post):
    post = preprocess_post(post)

    totalcontent = post['heading'] + '. ' + post['content']
    for reply in post['expertReplies']:
        totalcontent += reply['content']
    # To avoid MetaMap errors
    totalcontent = totalcontent.encode("ascii", errors="ignore").decode()
    result = metamap(nlp(totalcontent).sents)
    post.update(result)

    post['lastActivityTs'] = post.get('lastReplyTs', parse_timestamp(post['created']))
    post['numWords'] = len(re.findall(r'\w+', totalcontent))  # Count words
    post['replyByDoctor'] = False
    if forum == 'health24':
        post['replyByDoctor'] = True  #since all posts in health24 are replied by doctors

    post.pop('replies', None)  # Drop replies, only keep expertReplies
    post.pop('lastReplyTs', None)
    return post


in_fname, in_ext = INPUT_FILE.split('.')
out_fname = in_fname + '_mm.' + in_ext
with open(out_fname, 'w+') as out_file:
    with open(INPUT_FILE) as in_file:
        num_processed = 0
        processed_posts = []
        for line in in_file:
            print('Processing post %d' % (num_processed + 1))
            post = json.loads(line)
            processed_posts.append(json.dumps(process_post(post)))
            num_processed += 1
            if num_processed % BATCH_SIZE == 0:
                print('Writing batch #%d to file %s' %
                      (num_processed // BATCH_SIZE, out_fname))
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
