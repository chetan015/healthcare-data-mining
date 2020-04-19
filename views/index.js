 function drawChart(){
     d3.select("#chartArea").attr("class","container card bg-white");
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
        $("#mainArea").append("<div class='row'><div class='col-sm-4 pl-0'>"+chart_dom+legend_dom+"</div"+posts_dom+"</div>");
        
        var imgFileNames = ['webmd.png','patient.png','health24.png'];
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
                // $('#post').html(result);
                // var json_objects = JSON.parse(result);
                //drawChart(result[0]);
                for(var i = 0; i < result.length; i++){
                    // Build the dom for a post, which consists of the image, content and link dom elements
                    var content = result[i].content;
                    var link = result[i].link;
                    var heading = result[i].heading;
                    var group = result[i].group;
                    var trustworthiness = result[i].trustworthiness;
                    var hotness = result[i].hotness;
                    var freshness = result[i].freshness;
                    var length = result[i].length;
                    var imgFileName = "";
                    for(i=0;i<3;i++)
                    {
                        if(link.contains(imgFileNames[i]))
                            imgFileName = imgFileNames[i];
                            break;
                    }
                    
                    var image_dom = "<div class='col-2  my-auto'><img src="+imgFileName+" class='img-fluid' alt='Responsive image'></div>"
                    var content_dom = "<div class='col-9 pl-4 border-left'><div><h5>"+heading+"</h5><h6><i>"+group+"</i></h6><span>"+cotent+"</span><div class='row justify-content-center'><span class='icon'style='color:#15aabf'><i class='fas fa-user-nurse fa-lg'></i>"+trustworthiness+"</span><br><span class='icon' style='color:#f00c0c'><i class='fab fa-hotjar fa-lg'></i>"+hotness+"</span><br><span class='icon' style='color:#4c6ef5'><i class='far fa-calendar-alt fa-lg'></i>"+freshness+"</span><br><span class='icon' style='color:#f5a320'><i class='fas fa-ruler fa-lg'></i>"+length+"</span></div></div></div>"
                    var link_dom = "<div class='col-1 my-auto'><a href='"+link+"'><i class='fas fa-external-link-alt fa-lg'></i></a></div>"
                    var post_dom = "<div class = 'row py-3 post border-bottom' id = 'post'"+i+">"+image_dom+content_dom+link_dom+"</div";
                    $("#posts").append(post_dom)




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
        $("#mainArea").append("<div class='row'><div class='col-sm-4 pl-0'>"+chart_dom+legend_dom+"</div"+posts_dom+"</div>");
        
        var imgFileNames = ['webmd.png','patient.png','health24.png'];

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
                
                for(var i = 0; i < result.length; i++){
                    var content = result[i].content;
                    var link = result[i].link;
                    var heading = result[i].heading;
                    var group = result[i].group;
                    var trustworthiness = result[i].trustworthiness;
                    var hotness = result[i].hotness;
                    var freshness = result[i].freshness;
                    var length = result[i].length;
                    var imgFileName = "";
                    for(i=0;i<3;i++)
                    {
                        if(link.contains(imgFileNames[i]))
                            imgFileName = imgFileNames[i];
                            break;
                    }
                    
                    var image_dom = "<div class='col-2  my-auto'><img src="+imgFileName+" class='img-fluid' alt='Responsive image'></div>"
                    var content_dom = "<div class='col-9 pl-4 border-left'><div><h5>"+heading+"</h5><h6><i>"+group+"</i></h6><span>"+cotent+"</span><div class='row justify-content-center'><span class='icon'style='color:#15aabf'><i class='fas fa-user-nurse fa-lg'></i>"+trustworthiness+"</span><br><span class='icon' style='color:#f00c0c'><i class='fab fa-hotjar fa-lg'></i>"+hotness+"</span><br><span class='icon' style='color:#4c6ef5'><i class='far fa-calendar-alt fa-lg'></i>"+freshness+"</span><br><span class='icon' style='color:#f5a320'><i class='fas fa-ruler fa-lg'></i>"+length+"</span></div></div></div>"
                    var link_dom = "<div class='col-1 my-auto'><a href='"+link+"'><i class='fas fa-external-link-alt fa-lg'></i></a></div>"
                    var post_dom = "<div class = 'row py-3 post border-bottom' id = 'post'"+i+">"+image_dom+content_dom+link_dom+"</div";
                    $("#posts").append(post_dom)


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