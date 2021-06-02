function loginSuccess() {
    toastr.success("Trained Successfully")
    window.location.href = "/reg"
  }
  
  $( '#register' ).submit( function( e ) {
    $("#button").prop("disabled", true)
    $("#img").show()
    $.ajax( {
      url: '/train',
      type: 'POST',
      data: new FormData( this ),
      processData: false,
      contentType: false,
      success: function (response) {
        if (response === "success") {
          setTimeout(loginSuccess, 5000)
          swal
            .fire({
              icon: "success",
              title: "Training Successful",
            })
            .then((result) => {
              window.location.href = "/reg"
            })
        } else if (response === "error") {
          swal
            .fire({
              icon: "error",
              title: "Training Error",
              text: "Error while Training Face is not clear in ...!!!",
            })
            .then((result) => {
              $("#button").removeAttr("disabled")
              window.location.href = "/reg"

            })
        }
      },
      error: function (error) {
        console.log(error)
      }

    } );
    e.preventDefault();
  } );