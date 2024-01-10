
$(".ajax-call").click(function(){
    //var a = $("#ajax-data").val();
    var form = $(this).closest("form");
    var a = $(this).attr('data-value');
    console.log(a);
    $.ajax({
        url : form.attr("data-validate-ajax-url"),
        type: 'POST', 
        data : {
            'ajaxdata' : a
        },
        dataType : 'json',
        success: function(dataajax){
            var select = $("#type_pj");
            select.empty(); // Videz les options existantes
            dataajax.list_pj.forEach(function(item) {
            select.append('<option>' + item.name + '</option>');
        });
        },
        error: function(xhr, status, error) { // Error handling
        console.log("Error: " + error);
        console.log("Status: " + status);
        console.dir(xhr);
        }
    })
});




