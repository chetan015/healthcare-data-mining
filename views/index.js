$( document ).ready(function() {
    var api_url = 'http://127.0.0.1:5000/api/v1/search?'
    // var key = '5b578yg9yvi8sogirbvegoiufg9v9g579gviuiub8' // not real
  
    // disease query
    $("#btnSubmit_disease").click(function() {
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
                
                for(var i = 0; i < result.length; i++){
                    var content = result[i].content;
                    var link = result[i].link;
                    var link_dom = "<a href=" + link + ">" + link + "</a><br>";
                    var content_dom = "<div>" + content + "</div><br>";
                    var temp = $("<div class='container card bg-white'>")
                                    .append(link_dom)
                                    .append(content_dom)
                                    .css({"padding" : "20px","margin": "10px"});
                    $("#posts")
                        .append(temp)
                        // .append(link_dom)
                        // .append(content_dom)
                        // .addClass("container card bg-white")
                        .css({"padding" : "20px","margin": "auto"});
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
                    var link_dom = "<a href=" + link + ">" + link + "</a><br>";
                    var content_dom = "<div>" + content + "</div><br>";
                    var temp = $("<div class='container card bg-white'>")
                                    .append(link_dom)
                                    .append(content_dom)
                                    .css({"padding" : "20px","margin": "10px"});
                    $("#posts")
                        .append(temp)
                        // .append(link_dom)
                        // .append(content_dom)
                        // .addClass("container card bg-white")
                        .css({"padding" : "20px","margin": "auto"});
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