$(document).ready(function(){
    $('#groupname').keyup( function(e){
        var groupname = $('#groupname').val();

        if(groupname != ''){
  
           $.ajax({
              url: '/checkgroupname',
              type: 'post',
              data: {groupname: groupname},
              success: function(response){
                    if (response == "Available"){
                        
                        $('#facebutton').prop('disabled', false);
                        $('#fname_response').html(response).css({'color':'blue', 'text-align':'right'});
                    }else{
                        $('#facebutton').prop('disabled', true);
                        $('#fname_response').html(response).css({'color':'red', 'text-align':'right'});
                    }
               }
           });
        }else{
           $("#fname_response").html("");
        }
    })
})