	var list = loadJSON(function(json) {
	  console.log(json);
	});
            
        function constructTable(selector) { 
              
            // Getting the all column names 
            var cols = Headers(list, selector);   
   
            // Traversing the JSON data 
            for (var i = 0; i < list.length; i++) { 
                var row = $('<tr/>');    
                for (var colIndex = 0; colIndex < cols.length; colIndex++) 
                { 
                    var val = list[i][cols[colIndex]]; 
                      
                    // If there is any key, which is matching 
                    // with the column name 
                    if (val == null) val = "";   
                        row.append($('<td/>').html(val)); 
                } 
                  
                // Adding each row to the table 
                $(selector).append(row); 
            } 
        } 
          
        function Headers(list, selector) { 
            var columns = []; 
            var header = $('<tr/>'); 
              
            for (var i = 0; i < list.length; i++) { 
                var row = list[i]; 
                  
                for (var k in row) { 
                    if ($.inArray(k, columns) == -1) { 
                        columns.push(k); 
                          
                        // Creating the header 
                        header.append($('<th/>').html(k)); 
                    } 
                } 
            } 
              
            // Appending the header to the table 
            $(selector).append(header); 
                return columns; 
        }
		
		function loadJSON(callback) {   
		  var xobj = new XMLHttpRequest();
		  xobj.overrideMimeType("application/json");
		  xobj.open('GET', '../Jsons/Js1.json', true);
		  xobj.onreadystatechange = function () {
			if (xobj.readyState == 4 && xobj.status == "200") {
			  callback(JSON.parse(xobj.responseText));
			}
		  };
		  xobj.send(null);  
		}