$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
  });

  var csrf_token = "{{ csrf_token() }}";

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrf_token);
          }
      }
  });
  $(document).ready(function(){
    $('.collapsible').collapsible();
  });
  $(document).ready(function(){
    $(".datepicker").datepicker({
      format: "dd mmmm, yyyy",
      yearRange: 3,
      showClearBtn: true,
      i18n: {
          done: "Select"
      }
  });
})
$(document).ready(function(){
  $('select').formSelect();
});
$(document).ready(function(){
  $('.parallax').parallax();
});
      