
    $(function() {
      $("#dynamic_field_add").click(function (e) {
        e.preventDefault();
        $("#dynamic_field_append").append('<div class="d-flex dynamic_field_div"><div class="mr-auto pb-2"><input type="text" class="form-control form-control-user" style="width: 950px;" name="subject[]" placeholder="Enter Subject"></div><div class="align-self-center pb-2"><a href="#" class="dynamic_field_remove"><i class="fa fa-close fa-fw text-danger"></i></a></div></div>');
        $(".dynamic_field_focus").last().focus();
      });

      $("body").on("click", ".dynamic_field_remove", function (e) {
        e.preventDefault();
        $(this).closest('.dynamic_field_div').remove();
      });
    });
  