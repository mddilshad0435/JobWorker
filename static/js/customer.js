function show_job_process_customer(results) {
    let row;
    // console.log("process job",results)
    if (true) {
        $("#process_jobs").html('<tr><th>Title</th><th>Description</th><th>File</th><th>Status</th><th>Price</th><th>Action</th></tr>')
        var res = results;
        $.each(res, function (a,b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td class="desc-text">' + b.description + '</td>'
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td>' + b.current_status + '</td>'
            if (b.price!="null"){
                row = row + '<td>' + b.price + '</td>'
            }
            
            if (b.current_status == "submitted_and_price_quoted") {
                row = row + '<td><div class="parentbuttonflex"><div class="buttonflex">'
                row = row + '<p><button class="button" title="Accept" onclick=approve_jobs(' + b.id + ') ><i class="fa fa-check"></i></button></p>'
                row = row + '<p><button class="button" title="Reject" onclick=reject_jobs(' + b.id + ') ><i class="fa fa-times"></i></button></p>'
                row = row + '</div></div></td>'
            }
            if (b.current_status == "submitted_completed"){
                row = row + '<td><form method="post" action="/job/file_download/"><input type="hidden" id="jobid" name="jobid" value="' + b.id + '"/><button type="submit" style="background-color:powderblue;">Download</button></form>'
            }
            if ( b.current_status == "rejected" || b.current_status == "submitted_processing" || b.current_status == "submitted_waiting"){
                row = row + '<td>-</td>'
            }
            if (b.current_status == "started") {
                row = row + "<td>-</td>"
                row = row + '<td>-</td>'
            }
            row = row + '</tr>';
            $("#process_jobs").append(row);
            // console.log(row)
        })
    }
}

function approve_jobs(job_id) {
    $.ajax({
        type: 'POST',
        async: true,
        url: "/user/accpeted_job/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({ 'job_id': job_id }),
        success: function (data) {
            console.log(data)
            location.replace('/user/customer/')
        }
    })
}

function reject_jobs(job_id) {
    $.ajax({
        type: 'POST',
        async: true,
        url: "/user/reject_job/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({ 'job_id': job_id }),
        success: function (data) {
            console.log(data)
            location.replace('/user/customer/')
        }
    })
}

// function download_file(job_id){
//     $.ajax({
//         type: 'POST',
//         async: true,
//         url: "/job/download_file/",
//         dataType: "json",
//         contentType: "application/json",
//         data: JSON.stringify({'job_id': job_id}),
//         beforeSend: function(){
//             $('#loader').css("display","block")
//         },
//         success: function (response) {
//             $('#loader').css("display","none")
//             console.log(response)
//             alert(response['msg'])

//         },
//         error: function(response){
//             $('#loader').css("display","none")
//             alert(response['msg'])
//                 // err_txt.text(`${response['msg']}`);
            

//         }
//     })    
// }

function show_completed_posts_customer(results) {
    let row;
    // console.log(results)
    if (true) {
        $("#compeleted_post_table").html('<tr><th>Title</th><th>Description</th><th>File</th><th>Price</th><th>Uploaded File</th></tr>');
        var res = results;
        $.each(res, function (a, b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td>' + b.description + '</td>'
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td>' + b.price + '</td>'
            row = row + '<td><button type="button" onclick=download_file('+b.id+')>Download</button>'
            row = row + '</tr>';
            $("#compeleted_post_table").append(row);
        })
    }
}
