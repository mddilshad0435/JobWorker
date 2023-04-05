
function with_price(job_id) {
    console.log(job_id)
    var number = document.getElementById('price' + job_id).value;
    console.log(number)
    if (!number){
        alert("Please enter the price!")
    }

    $.ajax({
        type: 'POST',
        async: true,
        url: "/job/update_price/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({'price': number, 'job_id': job_id }),
        success: function (data) {
            console.log(data)
            location.replace('/user/superuser/')
        }
    })

}


function show_job_process_superuser(results,workers=null) {
    let row;
    console.log("process job",results)
    console.log("workers",workers)
    if (true) {
        $("#process_jobs").html('<tr class="row-border"><th>Title</th><th>Description</th><th>Price</th><th>File</th><th>Status</th><th>Quote/Assigned_to</th><th>Approved</th><th>s3Path</th></tr>')
        // $("#process_jobs").append('<hr>');
        var res = results;
        $.each(res, function (a,b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td class="desc-text" >' + b.description + '</td>'
            if (b.price != "null"){
                row = row + '<td>' + b.price + '</td>'
            }
            else {
                row = row + '<td> - </td>'
            }
            
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td>' + b.current_status + '</td>'
            if (b.current_status == "started") {
                row = row + '<td><input type="number" class="price" placeholder="Enter price" id="price' + b.id + '"></td>'
                row = row + '<td>'
                row = row + '<button class="button"  onclick=with_price(' + b.id + ')><i class="fa fa-check"></i></button>'
                row = row + '<td>-</td>'
                row = row + '</td>'
            }
            if (b.current_status == "submitted_waiting"){
                row = row + '<td>' + '<select name="worker" id="worker_id' + b.id + '">'
                $.each(workers, function (a, c) {
                    row = row + '<option value="' + c.id + '">' + c.email + '</option>'
                })
                row = row + '</select></td>'
                row = row + '<td><button class="button" onclick=assign_jobs(' + b.id + ')><i class="fa fa-check"></i></button></td>'
                row = row + '<td>-</td>'
            }
            if (b.current_status == "submitted_processing" ) {
                row = row + '<td>' + b.worker + '</td>'
                row = row + '<td>-</td>'
                row = row + '<td>-</td>'
            }
            if (b.current_status == "submitted_completed") {
                row = row + '<td>' + b.worker + '</td>'
                row = row + '<td><form method="post" action="/job/file_download/"><input type="hidden" id="jobid" name="jobid" value="' + b.id + '"/><button type="submit" style="background-color:powderblue;">Download</button></form>'
                row = row + '<td>' + b.file_path + '</td>'
            }
            if (b.current_status == "submitted_and_price_quoted" || b.current_status == "rejected" ) {
                row = row + '<td>-</td>'
                row = row + '<td>-</td>'
                row = row + '<td>-</td>'
            }
            row = row + '</tr>';
            $("#process_jobs").append(row);
        })
    }
}


function show_initiated_post_table(results) {
    let row;
    console.log(results)
    if (true) {
        $("#initiated_post_table").html('<tr><th>Title</th><th>Description</th><th>File</th><th>Price</th><th>action</th></tr>');
        var res = results;
        $.each(res, function (a, b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td>' + b.description + '</td>'
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td><input type="number" id="price' + b.id + '"></td>'
            row = row + '<td>'
            row = row + '<button class="button"  onclick=with_price(' + b.id + ')><i class="fa fa-check"></i></button>'
            row = row + '</td>'

            row = row + '</tr>';
            $("#initiated_post_table").append(row);
        })
    }
}

function show_waiting_for_approval_post_table(results) {
    let row;
    console.log(results)
    if (true) {
        $("#waiting_for_approval_post_table").html('<tr><th>Title</th><th>Description</th><th>File</th><th>Price</th></tr>');
        var res = results;
        $.each(res, function (a, b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td>' + b.description + '</td>'
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td>' + b.price + '</td>'
            row = row + '</tr>';
            $("#waiting_for_approval_post_table").append(row);
        })
    }
}

function assign_jobs(job_id) {
    assigned_worker = document.getElementById('worker_id' + job_id).value
    $.ajax({
        type: 'POST',
        async: true,
        url: "/job/assign_to/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({ 'worker_id': assigned_worker, 'job_id': job_id }),
        success: function (data) {
            console.log(data)
            location.replace('/user/superuser/')
        }
    })

}

function show_approved_post_table(results, workers) {
    let row;
    console.log("@@@@@@@@@@@")
    console.log(workers)
    if (true) {
        $("#approved_post_table").html('<tr><th>Title</th><th>Description</th><th>File</th><th>Price</th><th>Assigned_to</th><th>action</th></tr>');
        var res = results;
        $.each(res, function (a, b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td>' + b.description + '</td>'
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td>' + b.price + '</td>'

            row = row + '<td>' + '<select name="worker" id="worker_id' + b.id + '">'
            $.each(workers, function (a, c) {
                row = row + '<option value="' + c.id + '">' + c.username + '</option>'
            })
            row = row + '</select></td>'
            row = row + '<td><button class="button" onclick=assign_jobs(' + b.id + ')><i class="fa fa-check"></i></button></td>'

            row = row + '</tr>';
            $("#approved_post_table").append(row);
        })
    }
}

function show_rejected_post_table(results) {
    let row;
    console.log(results)
    if (true) {
        $("#rejected_post_table").html('<tr><th>Title</th><th>Description</th><th>File</th><th>Price</th></tr>');
        var res = results;
        $.each(res, function (a, b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td>' + b.description + '</td>'
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td>' + b.price + '</td>'
            row = row + '</tr>';
            $("#rejected_post_table").append(row);
        })
    }
}

function show_processing_post_table(results) {
    let row;
    if (true) {
        $("#processing_post_table").html('<tr><th>Title</th><th>Description</th><th>File</th><th>Price</th><th>Assigned_to</th></tr>');
        var res = results;
        $.each(res, function (a, b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td>' + b.description + '</td>'
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td>' + b.price + '</td>'
            row = row + '<td>' + b.worker + '</td>'

            row = row + '</tr>';
            $("#processing_post_table").append(row);
        })
    }
}

function show_completed_post_table(results) {
    let row;
    console.log(results)
    if (true) {
        $("#completed_post_table").html('<tr><th>Title</th><th>Description</th><th>File</th><th>Price</th><th>done_by</th><th>s3Path</th><th>Uploaded File</th></tr>');
        var res = results;
        $.each(res, function (a, b) {
            row = ""
            row = row + '<tr>'
            row = row + '<td>' + b.title + '</td>'
            row = row + '<td>' + b.description + '</td>'
            row = row + '<td><a href="/' + b.job_file_path + '" target="blank">File</a></td>'
            row = row + '<td>' + b.price + '</td>'

            row = row + '<td>' + b.done_by + '</td>'
            row = row + '<td>' + b.file_path + '</td>'
            row = row + '<td><button type="button" onclick=download_file('+b.id+')>Download</button>'
            row = row + '</tr>';
            $("#completed_post_table").append(row);
        })
    }
}
