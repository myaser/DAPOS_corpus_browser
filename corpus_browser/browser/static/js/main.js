$(document).ready(function(){
  $('.query-item input:radio').on('change',function(){
    $('.query-item input:radio').prop('disabled',true);
    $('.form-item').prop('disabled',true);
    $(this).prop('disabled',false);
    $(this).parent().parent().children().prop('disabled',false);
  });
})
