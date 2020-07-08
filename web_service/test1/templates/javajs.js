<script charset="utf-8" type="text/javascript">
       // this is called a javascript closure. it also wont run the code until the page is finished loading
       // and it protects the scope of your variables from other code you may later add to the page
       $(function() {
           var select_cat1 = $('#cat1'),
               select_cat2 = $('#cat2'),
               select_cat3 = $('#cat3'),
               select_cat4 = $('#cat4');

           select_cat1.on('change', function() {
               // fires when room selection changes
               getUpdatedSettings();
           });

           select_cat2.on('change', function() {
               // fires when day selection changes
               getUpdatedSettings();
           });
           select_cat3.on('change', function() {
               // fires when day selection changes
               getUpdatedSettings();
           });
           select_cat4.on('change', function() {
               // fires when day selection changes
               getUpdatedSettings();
           });

           function getUpdatedSettings() {
               // data to send back to the server
               var send = {
                   cat1: select_cat1.val(),
                   cat2: select_cat2.val()
                   cat3: select_cat3.val()
                   cat4: select_cat4.val()
               };

               // make the selections disabled while fetching new data
//               select_1am.attr('disabled', true);
//               select_2am.attr('disabled', true);

               $.getJSON("/_get_updated_settings", send, function(response) {
                   // this send the room and the day select vals to the URL specified
                   // we will need to add a handler for this in Flask

                   // for the purpose of the example I am assuming the response will be
                   // a JSON object that has a dictionary of elements ("am_1" and "am_2")
                   // each of which is a list of values for the selects....

                   console.log(response); // good for QA!

//                   // populate 1am
//                   select_1am.empty();
//                   $.each(response.am_1, function (index, value) {
//                       select_1am.append(
//                       $('<option>', {
//                           value: value,
//                           text: value
//                       }, '</option>'))
//                   });
//
//                   // populate 2am
//                   select_2am.empty();
//                   $.each(response.am_2, function (index, value) {
//                       select_2am.append(
//                       $('<option>', {
//                           value: value,
//                           text: value
//                       }, '</option>'))
//                   });
//
//                   // remove disabled now
//                   select_1am.removeAttr('disabled');
//                   select_2am.removeAttr('disabled');
               });
           }

       });
</script>