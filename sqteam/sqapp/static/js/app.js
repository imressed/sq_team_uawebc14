// Get the context of the canvas element we want to select

$(document).ready(function() {


// Get context with jQuery - using jQuery's .get() method.
var ctx = $("#myChart").get(0).getContext("2d");
// This will get the first returned node in the jQuery collection.

var data = {
    labels: ["Total amount of trips"],
    datasets: [
        {
            label: "Metro",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [65]
        },
        {
            label: "Train",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [59]
        },
        {
            label: "Bus",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [35]
        },
        {
            label: "Metro",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [41]
        },
        {
            label: "My First datassdset",
            fillColor: "rgba(220,20,220,0.2)",
            strokeColor: "rgba(220,20,220,1)",
            pointColor: "rgba(220,20,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,20,220,1)",
            data: [41]
        },
    ]
};

var myLineChart = new Chart(ctx).Bar(data);

    $('#period-select').on('change', function() {
    var csrftoken = $.cookie('csrftoken');
      $.ajax({
                    type: "GET",
                    url: '/load',
                    data: {

                        csrfmiddlewaretoken: csrftoken
                    }
                })
                .done(function(msg) {
                    alert(msg);
                });
    });

    $('#type-select').on('change', function() {
      alert( this.value ); // or $(this).val()
    });
});
