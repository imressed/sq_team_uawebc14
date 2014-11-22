// Get the context of the canvas element we want to selec

// Get context with jQuery - using jQuery's .get() method.
var ctx = $("#myChart").get(0).getContext("2d");
// This will get the first returned node in the jQuery collection.

var data = {
    labels: ["Total amount of trips"],
    datasets: [
        {
            label: "Amount",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [0]
        },
    ]
};

myLineChart = new Chart(ctx).Bar(data);

    $('#period-select').on('change', function() {
        var csrftoken = $.cookie('csrftoken');
        var period = $(this).val();
          $.ajax({
                type: "GET",
                url: '/load',
                data: {
                    period: period,
                    csrfmiddlewaretoken: csrftoken
                }
            })
            .done(function(msg) {
                //myLineChart.datasets[0].data[0].value = parseInt(msg);
                myLineChart.datasets[0].bars[0].value = parseInt(msg);
                myLineChart.update();
            });
    });

        $('#type-select').on('change', function() {
            var csrftoken = $.cookie('csrftoken');
            var type = $(this).val();
            $.ajax({
                type: "GET",
                url: '/load',
                data: {
                    type: type,
                    csrfmiddlewaretoken: csrftoken
                }
            })
            .done(function(msg) {
                myLineChart.datasets[0].bars[0].value = parseInt(msg);
                myLineChart.update();
            });
        });
