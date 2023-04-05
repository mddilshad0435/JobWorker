function data_to_dict(serializedData) {
    data = {}
    for (var i = 0; i < serializedData.length; i++) {
        data[serializedData[i]['name']] = serializedData[i]['value']
    }
    return data
}

$("#password_reset_form").submit(function (e) {
    e.preventDefault();
    var serializedData = $(this).serializeArray();
    serializedData['token'] = localStorage.getItem("token")
    data = data_to_dict(serializedData)
    console.log(data)
    $.ajax({
        type: 'POST',
        url: "/user/password_reset/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(data),
        processData: false,
        success: function (data) {
            localStorage.removeItem("token");
            location.replace('/home/')
        },
        error: function (response) {
            console.log(response)
            console.log('error')
            // var err_txt = $('#password-id-error-txt');
            // if (err_txt.hasClass('d-block')) {
            //     err_txt.removeClass('d-block');
            //     err_txt.addClass('d-none');
            // }
            // if (err_txt.hasClass('d-none')) {
            //     err_txt.addClass('d-block');
            //     err_txt.text(`${response.responseJSON['msg']}`);
            // }
            alert(response.responseJSON['msg'])
        }
    })
})


$("#signup_form").submit(function (e) {
    e.preventDefault();
    var serializedData = $(this).serializeArray();
    data = data_to_dict(serializedData)
    console.log(serializedData[0])
    console.log(data)
    $.ajax({
        type: 'POST',
        url: "/user/signup/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (data) {
            console.log(data)
            // localStorage.setItem("token", data['token']);

            if (data['user_type'] == 3) {
                location.replace("/user/customer/")
            }

            else if (data['user_type'] == 2) {
                location.replace('/user/worker/')
            }

            else {
                location.replace('/user/superuser/')
            }
        },
        error: function (response) {
            console.log(response.responseJSON.msg)
           
            alert(response.responseJSON.msg)
        }
    })
}
)

$("#worker_signup_form").submit(function (e) {
    e.preventDefault();
    var serializedData = $(this).serializeArray();
    data = data_to_dict(serializedData)
    console.log(serializedData[0])
    console.log(data)
    $.ajax({
        type: 'POST',
        url: "/user/signup/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (data) {
            console.log(data)
            location.replace('/user/superuser/')
        },
        error: function (response) {
            console.log(response)
            console.log('error')
            
            alert(response.responseJSON['msg'])
            
        }
    })
})





$("#login_form").submit(function (e) {
    e.preventDefault();
    var serializedData = $(this).serializeArray();
    data = data_to_dict(serializedData)

    $.ajax({
        type: 'POST',
        url: "/user/login/",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (data) {
            console.log(data)
            // localStorage.setItem("token", data['token']);

            if (data['user_type'] == 3) {
                location.replace("/user/customer/")
            }

            else if (data['user_type'] == 2) {
                location.replace('/user/worker/')
            }

            else {
                location.replace('/user/superuser/')
            }

        },
        error: function (response) {
            console.log(response)
            alert(response.responseJSON.msg)
        }
    })
})

$(document).ready(function(){
    $("#create_post").submit(function (e) {
        e.preventDefault();
        const form_id = document.getElementById('create_post');
        var formData = new FormData(form_id);
        formData.append('access_token', localStorage.getItem("token"))
        $.ajax({
            type: 'POST',
            url: "/create_job/",
            async: true,
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                console.log(data)
                location.replace('/user/customer/')
            },
            error: function (response) {
                console.log(response)
            }
        })
    })
});

function get_location(data, myArraySplit) {
    if (data['user_type'] == 0) {
        location.replace('/home/')
    }
    let arr = ['create_worker','details','security','collections','about','intro'];
    if (data['user_type'] == 1) {
        if (myArraySplit[myArraySplit.length - 2] != 'superuser') {
            if (!arr.includes(myArraySplit[myArraySplit.length - 2])) {
                location.replace('/user/superuser/')
            }
        }
    }
    if (data['user_type'] == 2) {
        if (myArraySplit[myArraySplit.length - 2] != 'worker') {
            
            if (!arr.includes(myArraySplit[myArraySplit.length - 2])) {
                location.replace('/user/worker/')
            }
        }
    }
    if (data['user_type'] == 3) {
        if (myArraySplit[myArraySplit.length - 2] != 'customer') {
            if (!arr.includes(myArraySplit[myArraySplit.length - 2])) {
                location.replace('/user/customer/')
            }
        }
        
    }
}

function setLogout(){
    $("#loginOrlogout").html('<a onclick="logout()" class="btn btn-primary w-100" target="_blank" rel="noopener">&nbsp;Logout</a>')
}
function setLogin(){
    $("#loginOrlogout").html('<a href="/user/login/" class="btn btn-primary w-100" target="_blank" rel="noopener">&nbsp;Login</a>')

}
function setAccountDetails(){
    $(".accountDetails").css("display","block");
    $(".accountUser").css("display","none")
}

window.onload = function () {

    let searchText = "";
    const u = window.location.href;
    const myArraySplit = u.split("/");
    console.log(myArraySplit);
    // tokens = localStorage.getItem("token");
    console.log(myArraySplit[myArraySplit.length - 2]);
    // console.log(tokens)
    if (true) {
        $.ajax({
            type:'POST',
            async: true,
            url: "/user_type/",
            success: function(data){
                console.log(data)
                setLogout()
                setAccountDetails()
                get_location(data, myArraySplit);
            },
            error: function(data){
                console.log(data.responseJSON['msg'])
                setLogin()
            }
        })
    }

    if (myArraySplit[myArraySplit.length - 2] == 'customer') {
        $.ajax({
            type: 'POST',
            async: true,
            url: "/user/customer/",
            dataType: "json",
            contentType: "application/json",
            // data: JSON.stringify({ 'data': null }),
            success: function (data) {
                console.log("*******",data)
                show_job_process_customer(data['main_jobs'])
            },
            error: function(data){
                location.replace(data.responseJSON['url'])
            }
        })
    }
    if (myArraySplit[myArraySplit.length - 2] == 'worker') {
        $.ajax({
            type: 'POST',
            async: true,
            url: "/user/worker/",
            dataType: "json",
            contentType: "application/json",
            // data: JSON.stringify({ 'access_token': tokens }),
            success: function (data) {
                show_all_worker_jobs(data['all_jobs'])
            },
            error: function(data){
                // location.replace('/home/')
                location.replace(data.responseJSON['url'])
            }
        })
    }
    if (myArraySplit[myArraySplit.length - 2] == 'superuser') {
        $.ajax({
            type: 'POST',
            async: true,
            url: "/user/superuser/",
            dataType: "json",
            contentType: "application/json",
            // data: JSON.stringify({ 'access_token': "null" }),
            success: function (data) {
                show_job_process_superuser(data['main_jobs'],data['workers'])
            },
            error: function(data){
                console.log(data.responseJSON['url'])
                // localStorage.setItem("token", "");
                location.replace(data.responseJSON['url'])
            }
        })
    }
    if (myArraySplit[myArraySplit.length - 2] == 'create_worker') {
        $.ajax({
            type: 'POST',
            async: true,
            url: "/user/superuser_valid/",
            dataType: "json",
            contentType: "application/json",
            // data: JSON.stringify({ 'access_token': tokens }),
            success: function (data) {
            },
            error: function (response) {
                data = response.responseJSON
                if (data['user_type'] == 2) {
                    location.replace('/user/worker/')
                }

                else {
                    location.replace('/user/customer/')
                }
            }
        })
    }
    
    if (myArraySplit[myArraySplit.length - 2] == 'details'){
        $.ajax({
            type: 'POST',
            async: true,
            url: "/user/details/",
            dataType: "json",
            contentType: "application/json",
            // data: JSON.stringify({ 'access_token': tokens }),
            success: function (data) {
                console.log("account details",data)
                user_detail_fill(data.details,data.countries, data.address,data.states, data.cities)
                // location.replace('/')
            },
            error: function(data){
                localStorage.setItem("token", "");
                location.replace('/user/login/')
            }
        })
    }
    if (myArraySplit[myArraySplit.length - 2] == 'security'){
        $.ajax({
            type: 'POST',
            async: true,
            url: "/user/security/",
            dataType: "json",
            contentType: "application/json",
            // data: JSON.stringify({ 'access_token': tokens }),
            success: function (data) {
                console.log("account details",data)
                user_email_name_fill(data.details)
                // location.replace('/')
            },
            error: function(data){
                localStorage.setItem("token", "");
                location.replace('/user/login/')
            }
        })
    }
    if (myArraySplit[myArraySplit.length - 2] == 'collections'){
        $.ajax({
            type: 'POST',
            async: true,
            url: "/user/collections/",
            dataType: "json",
            contentType: "application/json",
            // data: JSON.stringify({ 'access_token': tokens }),
            success: function (data) {
                console.log("account details",data)
                user_email_name_fill(data.details)
                // location.replace('/')
            },
            error: function(data){
                localStorage.setItem("token", "");
                location.replace('/user/login/')
            }
        })
    }
}

function logout() {
    $.ajax({
        type: "POST",
        url: "/user/logout/",
        success: function(data){
            location.replace('/user/login/');
        }
    })    
}

function user_detail_fill(result,countries,address,states,cities){
    $("#username").append(result.first_name)
    $("#useremail").append(result.email)
    $("#fn").val(result.first_name)
    $("#ln").val(result.last_name)
    $("#email").val(result.email)
    if (result.mobile != 'None'){
        $("#phone").val(result.mobile)
    }
    if (result.bio != 'None'){
        $("#bio").val(result.bio)
    }
    let row;
    // console.log(countries)
    if (true) {
        var res = countries;
        row=""
        row = row + '<option value="">' +"" + '</option>'
        $.each(res, function (a, c) {
            if (address.country_id && address.country_id==c.id){
                row = row + '<option value="' + c.id + '" selected>' + c.name + '</option>'
            }
            else {
                row = row + '<option value="' + c.id + '">' + c.name + '</option>'
            }
        })
        $("#country").append(row)
    }
    console.log(address)
    if (address.country_id){
        console.log(states)
        $("#zip").val(address['zipCode'])
        $("#address1").val(address['address1'])
        $("#address2").val(address['address2'])
        //Adding states
        let row;
        var res = states;
        row=""
        $.each(res, function (a, c) {
            if (address.state_id==c.id){
                row = row + '<option value="' + c.id + '" selected>' + c.name + '</option>'
            }
            else {
                row = row + '<option value="' + c.id + '">' + c.name + '</option>'
            }
            
        })
        $("#state").append(row)
        $("#city").html("")
       
        var res = cities;
        row = ""
        $.each(res, function(a, c){
            if (address.city_id==c.id){
                row = row + '<option value="' + c.id + '" selected>' + c.name + '</option>'
            }
            else {
                row = row + '<option value="' + c.id + '">' + c.name + '</option>'
            }
        })
        $("#city").append(row)
    }
}

$("#country").change(function () {
    countryId = $(this).val()
    console.log("country id",countryId)
    $.ajax({      
        type: "POST",
        url: "/states/",                 
        data:JSON.stringify(countryId),
        success: function (data) { 
            console.log(data.states);
            let row;
            $('#state').html("")
            if (true) {
                var res = data.states;
                row=""
                $.each(res, function (a, c) {
                    row = row + '<option value="' + c.id + '">' + c.name + '</option>'
                })
                $("#state").append(row)
            }
        }
    });
  });

$("#state").change(function () {
    stateId = $(this).val()
    countryId = $("#country").val()
    console.log("stateId",stateId,countryId)
    data = {
        "stateId":stateId,
        "countryId": countryId
    }
    $.ajax({
        type: "POST",
        url: "/cities/",
        data: JSON.stringify(data),
        success: function (data) {
            console.log(data.cities)
            $("#city").html("")
            let row;
            var res = data.cities;
            row = ""
            $.each(res, function(a, c){
                row = row + '<option value="' + c.id + '">' + c.name + '</option>'
            })
            $("#city").append(row)
        }
    })
})



function user_email_name_fill(result){
    $("#username").append(result.fullname)
    $("#useremail").append(result.email)
}

$("#passwordReset").submit(function (e) {
    e.preventDefault()
    var data = $(this).serializeArray();
    data = data_to_dict(data)
    if (data.new_password != data.cnp ){
        alert("Password Not match")
    }
    else if (data.old_password == data.new_password) {
        alert("Old password and new password mus not be same!")
    }
    else {
        delete data.cnp
        $.ajax({
            type: "POST",
            url: "/user/reset_password/",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(data),
            processData: false,
            success: function(data){
                alert("Password change succesfully")
                location.reload()
            },
            error: function(error){
                console.log("in error",error)
                alert(error.responseJSON['msg'])
            }
        })
    }
    
})
$("#cencelReset").click(function () {
    location.reload();
})
$("#cencelReset1").click(function () {
    location.reload();
})

$("#userDetailsForm").submit(function(e) {
    e.preventDefault()
    var serializedData = $(this).serializeArray();
    console.log("data before",serializedData)
    serializedData = data_to_dict(serializedData)
    console.log("data",serializedData)
    if (!serializedData.mobile){
        delete serializedData.mobile
    }
    console.log("data",serializedData)
    $.ajax({
        type: "POST",
        url: "/user/alldetails/",
        dataType: "json",
        contentType: "application/json",
        processData: false,
        async: true,
        data: JSON.stringify(serializedData),
        success: function(data){
            console.log("success",data)
            location.reload()
        },
        error: function(error){
            console.log("error",error)
            alert(error.responseJSON['msg'])
            location.reload()
        }
    })
})

$("#adressform").submit(function (e){
    e.preventDefault()
    var serializedData = $(this).serializeArray();
    serializedData = data_to_dict(serializedData)
    zip = serializedData['zip']
    console.log(serializedData)
    if (zip.length !=6) {
        alert("ZipCode must be six digit number!")
    }
    else {
        $.ajax({
            type: "POST",
            url: "/user/address/",
            dataType: "json",
            contentType: "application/json",
            processData: false,
            async: true,
            data: JSON.stringify(serializedData),
            success: function(data){
                console.log("in success",data)
                alert(data['msg'])
                location.reload()
            },
            error: function (error) {
                console.log("in error", error)
                alert(data['msg'])
                location.reload()
            }
        })
    }
    
})

// $("#exampleModal").on
// $('#exampleModal').onclick('show.bs.modal', function (event) {
//     var button = $(event.relatedTarget) // Button that triggered the modal
//     var recipient = button.data('whatever') // Extract info from data-* attributes
//     // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
//     // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
//     var modal = $(this)
//     modal.find('.modal-title').text('New message to ' + recipient)
//     modal.find('.modal-body input').val(recipient)
//   })
  