window.isFetching = false, window.statements = false, window.dash;
function DashXBlock(runtime, element) {
	
	$(element).find('.cancel-button').click(function() {
        runtime.notify('cancel', {});
    });
	
	$(element).find('.save-button').bind('click', function() {
        runtime.notify('cancel', {});
        
        var handlerUrl = runtime.handlerUrl(element, 'update_dashboard');
        var outObj = {};
        
        
        outObj.width = $(element).find('#edit_width').val();
        outObj.height = $(element).find('#edit_height').val();
        outObj.display_name = $(element).find('#edit_display_name').val();
        
        $.post(handlerUrl, JSON.stringify(outObj), function(res){
        
			console.log("This is the response: ", res);
		});
        
        
    });
	
    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });
		
	var chartID = ('r' + Math.random()).replace('.', '');
	$(element).find('.chart').attr('id', chartID);
	
	if(isFetching == false){
		isFetching = true;
		
		ADL.XAPIWrapper.changeConfig({endpoint: 'https://lrs.adlnet.gov/xAPI/'});
		dash = new ADL.XAPIDashboard();
		
		var since = (new Date(Date.now() - 1000 * 60 * 60 * 24 * 14)).toISOString();
		dash.fetchAllStatements({since: since}, function(data){
			statements = true;
			makeChart();
		});
	}
	else{
		var i  = window.setInterval(function(){
			if(statements){
				window.clearInterval(i);
				makeChart();
			}
		}, 1000);
	}
	
	function makeChart(){
		var chart = dash.createBarChart({
			container: '#' + chartID,
			groupBy: 'actor.mbox',
			post: function(data){
				data.orderBy('out', 'desc').slice(0, 10);
			},
			customize: function(chart){
				chart.xAxis.rotateLabels(45);
			}
		});
		chart.draw();
	}
}
