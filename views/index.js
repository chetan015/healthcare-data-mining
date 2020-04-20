 function drawChart(data){
    // d3.select("#chartArea").attr("class","container card bg-white");
    const margin = 50;
    const offsetWidth = document.getElementById("chartArea").offsetWidth;
    const offsetHeight = 300;
    const width = (offsetWidth - 2*margin);
    const height = offsetHeight - 2*margin;
    var chartDiv = d3.select("#chartArea").attr("height",offsetHeight);
    console.log(data);
    // data = [{symptom:"Fever",posts:700},{symptom:"Cough",posts:600},{symptom:"Cold",posts:500}]

    var svg = chartDiv.append("svg").attr("width",offsetWidth-30).attr("height",offsetHeight);

    const chart = svg.append('g')
                    .attr('transform', `translate(${margin}, ${margin})`);

    const yScale = d3.scaleLinear()
                    .range([height, 10])
                    .domain([0,Math.ceil((d3.max(data.map(s=>s.posts)))/10)*10]);

    chart.append('g')
        .call(d3.axisLeft(yScale));

    const xScale = d3.scaleBand()
        .range([0, width])
        .domain(data.map(s=>s.symptom))
        .padding(0.2)

    chart.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(xScale));
    // console.log(s);
    // console.log(function(data){return data.map((s) =>(s.posts))})
    chart.selectAll()
        .data(data)
        .enter()
        .append('rect')
        .attr('x', (d) => xScale(d.symptom))
        // .attr('transform', 'rotate(-90)')
        .attr('y',height)
        .attr('height',0)
        .attr('width', xScale.bandwidth())
        .attr("fill", "#15aabf")
        .transition().duration(1000)
        .attr('y',(d)=>yScale(d.posts))
        .attr('height', (s) => height - yScale(s.posts))
        ;
    chart.append("text")
    .attr("x", (width / 2))
    .attr("y", -5)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .text("Most Reported Symptoms");
 }
 
 $( document ).ready(function() {
    var api_url = 'http://127.0.0.1:5000/api/v1/search?'
    // var key = '5b578yg9yvi8sogirbvegoiufg9v9g579gviuiub8' // not real
  
    // disease query
    $("#btnSubmit_disease").click(function() {
        // Set the layout for displaying the visualization, legend and results
        var chart_dom = "<div class='card mb-3' id='chartArea'></div>";
        var legend_dom = "<div class='card pl-5 pb-4'><span class='icon'style='color:#15aabf'><i class='fas fa-user-nurse fa-lg'></i>Trustworthiness</span><br><span class='icon' style='color:#f00c0c'><i class='fab fa-hotjar fa-lg'></i>Hotness</span><br><span class='icon' style='color:#4c6ef5'><i class='far fa-calendar-alt fa-lg'></i>Freshness</span><br><span class='icon' style='color:#f5a320'><i class='fas fa-ruler fa-lg'></i>Length</span></div>";
        var posts_dom = "<div class='col-sm-8 card container' id='posts'></div>";
        $('#mainArea').empty();
        $("#mainArea").append("<div class='row'><div class='col-sm-4 pl-0'>"+chart_dom+legend_dom+"</div>"+posts_dom+"</div>");
        
        // var imgFileNames = ['webmd.png','patient.png','health24.png'];
        var placeholder = $("#input_disease").attr('placeholder');
        var query_term = $("#input_disease").val();
        var query = "query_term=" + query_term + "&query_type=" + placeholder;
        $.ajax({
            url: api_url + query,
            crossOrigin: true, 
            async: true,         
            contentType: "application/json",
            dataType: 'json',
            type: 'GET',
            success: function(result){
                console.log(result);
                // return;
                // $('#post').html(result);
                // var json_objects = JSON.parse(result);
                drawChart(result[result.length - 1]);
                for(var i = 0; i < result.length - 1; i++){
                    // Build the dom for a post, which consists of the image, content and link dom elements
                    var site = result[i].site;
                    var content = result[i].content;
                    content = content[0].slice(0, 500);
                    content = content.concat("....")
                    console.log(content);
                    var link = result[i].link;
                    var heading = result[i].heading;
                    var group = result[i].group;
                    var trusthworthiness = result[i].trusthworthiness;
                    var hotness = result[i].hotness;
                    hotness = Math.round((hotness + Number.EPSILON) * 100) / 100
                    var freshness = result[i].freshness;
                    freshness = Math.round((freshness + Number.EPSILON) * 100) / 100
                    var length = result[i].length;
                    length = Math.round((length + Number.EPSILON) * 100) / 100
                    var imgFileName = site + ".png";
                    
                    // for(i=0;i<3;i++)
                    // {
                    //     if(link.includes(imgFileNames[i]))
                    //         imgFileName = imgFileNames[i];
                    //         break;
                    // }

                    var image_dom = "<div class='col-2  my-auto'><img src='" + imgFileName + "' class='img-fluid' alt='Responsive image'></div>"
                    var content_dom = "<div class='col-9 pl-4 border-left'><div><h5>" + heading + "</h5><h6><i>" + group + "</i></h6><span>" + content + "</span><div class='row justify-content-center'><span class='icon'style='color:#15aabf'><i class='fas fa-user-nurse fa-lg'></i>" + trusthworthiness + "</span><br><span class='icon' style='color:#f00c0c'><i class='fab fa-hotjar fa-lg'></i>" + hotness + "</span><br><span class='icon' style='color:#4c6ef5'><i class='far fa-calendar-alt fa-lg'></i>"+freshness+"</span><br><span class='icon' style='color:#f5a320'><i class='fas fa-ruler fa-lg'></i>"+length+"</span></div></div></div>"
                    var link_dom = "<div class='col-1 my-auto'><a href='"+link+"'><i class='fas fa-external-link-alt fa-lg'></i></a></div>"
                    var post_dom = "<div class = 'row py-3 post border-bottom' id = 'post"+i+"'>"+image_dom+content_dom+link_dom+"</div";
                    $("#posts").append(post_dom)
                    // return;

                    // var content = result[i].content;
                    // var link = result[i].link;
                    // var link_dom = "<a href=" + link + ">" + link + "</a><br>";
                    // var content_dom = "<div>" + content + "</div><br>";
                    // var temp = $("<div class='container card bg-white'>")
                    //                 .append(link_dom)
                    //                 .append(content_dom)
                    //                 .css({"padding" : "20px","margin": "10px"});
                    // $("#posts")
                    //     .append(temp)
                    //     // .append(link_dom)
                    //     // .append(content_dom)
                    //     // .addClass("container card bg-white")
                    //     .css({"padding" : "20px","margin": "auto"});
                }
                // console.log(json_objects);

                // var link = "https://www.w3schools.com/jquery/";    
                // var records = "";
                // var l = "";

                // records += "<div>" + JSON.stringify(result) + "</div>";
                // l += "<a href=" + link + ">" + link + "</a>";

            
                // $("#post #link").attr("href", link).html(link);
                // $("#post_content").html(JSON.stringify(result));


                // $("#posts").append(records);
                // $("#posts").append(l);
            },
            error: function(xhr, status, error){
                alert(xhr + status + error);
            }
        })
    });

    // symptom query
    $("#btnSubmit_symptom").click(function() {
        var chart_dom = "<div class='card mb-3' id='chartArea'></div>";
        var legend_dom = "<div class='card pl-5 pb-4'><span class='icon'style='color:#15aabf'><i class='fas fa-user-nurse fa-lg'></i>Trustworthiness</span><br><span class='icon' style='color:#f00c0c'><i class='fab fa-hotjar fa-lg'></i>Hotness</span><br><span class='icon' style='color:#4c6ef5'><i class='far fa-calendar-alt fa-lg'></i>Freshness</span><br><span class='icon' style='color:#f5a320'><i class='fas fa-ruler fa-lg'></i>Length</span></div>";
        var posts_dom = "<div class='col-sm-8 card container' id='posts'></div>";
        $('#mainArea').empty();
        $("#mainArea").append("<div class='row'><div class='col-sm-4 pl-0'>"+chart_dom+legend_dom+"</div>"+posts_dom+"</div>");
        
        // var imgFileNames = ['webmd.png','patient.png','health24.png'];

        var placeholder = $("#input_symptom").attr('placeholder');
        var query_term = $("#input_symptom").val();
        var query = "query_term=" + query_term + "&query_type=" + placeholder;
        $.ajax({
            url: api_url + query,
            crossOrigin: true, 
            async: true,         
            contentType: "application/json",
            dataType: 'json',
            type: 'GET',
            success: function(result){
                console.log(result);
                // $('#post').html(result);
                // var json_objects = JSON.parse(result);
                drawChart(result[result.length - 1]);
                for(var i = 0; i < result.length - 1; i++){
                    var site = result[i].site;
                    var content = result[i].content;
                    content = content[0].slice(0, 500);
                    content = content.concat("....")
                    var link = result[i].link;
                    var heading = result[i].heading;
                    var group = result[i].group;
                    var trusthworthiness = result[i].trusthworthiness;
                    var hotness = result[i].hotness;
                    hotness = Math.round((hotness + Number.EPSILON) * 100) / 100
                    var freshness = result[i].freshness;
                    freshness = Math.round((freshness + Number.EPSILON) * 100) / 100
                    var length = result[i].length;
                    length = Math.round((length + Number.EPSILON) * 100) / 100
                    var imgFileName = site + ".png";

                    // var imgFileName = "";
                    // for(i=0;i<3;i++)
                    // {
                    //     if(link.includes(imgFileNames[i]))
                    //         imgFileName = imgFileNames[i];
                    //         break;
                    // }
                    
                    var image_dom = "<div class='col-2  my-auto'><img src='" + imgFileName + "' class='img-fluid' alt='Responsive image'></div>"
                    var content_dom = "<div class='col-9 pl-4 border-left'><div><h5>" + heading + "</h5><h6><i>" + group + "</i></h6><span>" + content + "</span><div class='row justify-content-center'><span class='icon'style='color:#15aabf'><i class='fas fa-user-nurse fa-lg'></i>" + trusthworthiness + "</span><br><span class='icon' style='color:#f00c0c'><i class='fab fa-hotjar fa-lg'></i>" + hotness + "</span><br><span class='icon' style='color:#4c6ef5'><i class='far fa-calendar-alt fa-lg'></i>"+freshness+"</span><br><span class='icon' style='color:#f5a320'><i class='fas fa-ruler fa-lg'></i>"+length+"</span></div></div></div>"
                    var link_dom = "<div class='col-1 my-auto'><a href='"+link+"'><i class='fas fa-external-link-alt fa-lg'></i></a></div>"
                    var post_dom = "<div class = 'row py-3 post border-bottom' id = 'post"+i+"'>"+image_dom+content_dom+link_dom+"</div";
                    $("#posts").append(post_dom)
                    // return;

                    // var content = result[i].content;
                    // var link = result[i].link;
                    // var link_dom = "<a href=" + link + ">" + link + "</a><br>";
                    // var content_dom = "<div>" + content + "</div><br>";
                    // var temp = $("<div class='container card bg-white'>")
                    //                 .append(link_dom)
                    //                 .append(content_dom)
                    //                 .css({"padding" : "20px","margin": "10px"});
                    // $("#posts")
                    //     .append(temp)
                    //     // .append(link_dom)
                    //     // .append(content_dom)
                    //     // .addClass("container card bg-white")
                    //     .css({"padding" : "20px","margin": "auto"});
                }
                // console.log(json_objects);

                // var link = "https://www.w3schools.com/jquery/";    
                // var records = "";
                // var l = "";

                // records += "<div>" + JSON.stringify(result) + "</div>";
                // l += "<a href=" + link + ">" + link + "</a>";

            
                // $("#post #link").attr("href", link).html(link);
                // $("#post_content").html(JSON.stringify(result));


                // $("#posts").append(records);
                // $("#posts").append(l);
            },
            error: function(xhr, status, error){
                alert(xhr + status + error);
            }
        })
    });


  });