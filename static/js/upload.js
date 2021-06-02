function loginSuccess(count) {
  toastr.success("Uploaded Successfully Attendance Marked for "+count+" Students");
  window.location.href = "/identify";
}

$("#register").submit(function (e) {
  $("#img").show();
  $.ajax({
    url: "/upload",
    type: "POST",
    data: new FormData(this),
    processData: false,
    contentType: false,
    success: function (response) {
      if (response === "error") {
        swal
          .fire({
            icon: "error",
            title: "Error in Image",
            text: "No Face Found in Image please Upload Clear Image",
          })
          .then((result) => {
            $("#button").removeAttr("disabled");
            window.location.href = "/identify";
          });
      } else {
        swal
          .fire({
            icon: "success",
            title: "Attendnace Marked Succesfully for "+response.length+" Students",
          })
          .then((result) => {
            window.location.href = "/identify";
          });
          setTimeout(loginSuccess(response.length), 9000);
        
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
  e.preventDefault();
});
