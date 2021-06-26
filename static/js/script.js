//Main JS file
$(document).ready(function(){
    //Initializes mobile sidenav
    $('.sidenav').sidenav({edge: "right"});
    //Initializes collapsible articles container
    $('.collapsible').collapsible();
    //Initializes form select fields
    $('select').formSelect();
    //Initializes parallax container
    $('.parallax').parallax();
    //Initializes delete modal alerts
    $('.modal').modal();
    //Initializes topics menu dropdown
    $('.dropdown-trigger').dropdown();
    //Initializes datepicker
    $(".datepicker").datepicker({
      format: "dd mmmm, yyyy",
      yearRange: 3,
      showClearBtn: true,
      i18n: {
          done: "Select"
      }
   });
  });

//CSRF Token
  var csrf_token = "{{ csrf_token() }}";

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrf_token);
          }
      }
  });
 
 


      