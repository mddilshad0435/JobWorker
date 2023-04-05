function job_complete(worker_job_id) {
    // job_s3_path = document.getElementById('complete_job_' + worker_job_id).value;
    // console.log(job_s3_path)
    console.log("yes")
    $.ajax({
        type: 'POST',
        async: true,
        url: "/job/complete/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({ 'worker_job_id': worker_job_id }),
        success: function (data) {
            console.log(data)
            location.replace('/user/worker/')
        },
        error: function(response){
            console.log(response)
            var err_txt = $('#credentials-id-error-txt');
            if (err_txt.hasClass('d-block')) {
                err_txt.removeClass('d-block');
                err_txt.addClass('d-none');
            }
            if (err_txt.hasClass('d-none')) {
                err_txt.addClass('d-block');
                err_txt.text(`${response.responseJSON['msg']}`);
            }
        }
    })
}
function show_all_worker_jobs(results) {
    let row;
    console.log("here",results)
    if (true) {
        $('#all_job').html('<tr><th>Title</th><th>Description</th><th>Status</th><th>Action</th></tr>');
        var res = results;
        $.each(res, function (a,b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td>' + b.description + '</td>'
            row = row + '<td>' + b.current_status + '</td>'
            if (b.current_status == "submitted_processing"){
                row = row + '<td><button type="button" style="background-color:powderblue;" onclick=job_complete(' + b.id + ')>Processed</button></td>'
            }
            else {
                row = row + '<td><form method="post" action="/job/file_download/"><input type="hidden" id="jobid" name="jobid" value="' + b.id + '"/><button type="submit" style="background-color:powderblue;">Download</button></form>'
            }
            
            row = row + '</tr>';
            $("#all_job").append(row);
        })
    }
}
