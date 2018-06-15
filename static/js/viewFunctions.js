function dynamicChoiceGenerator(choice_id, params){
    //dispatch id to the right function
}

function searchSetup(name, item, keyArgs, termArg){
    function getURL(base_url, item, key, term){
        var paramStr = '?item='+item;
        if(key != null){
            paramStr += '&key='+key;
        }
        if(term != null){
            paramStr += '&term='+term;
        }
        return base_url+paramStr;
    }
    var $select = $('#'+name+"_result");
    var $search = $('#'+name+"_search");
    $($search).on("change paste keyup", function() {
        $select.html('');
        var base_url = "http://127.0.0.1:8000/console/admin/search";
        var searchTerm = $(this).val();
        if (searchTerm.length > 2){
            termQuery = {};
            termQuery[termArg] = searchTerm;
            var test = getURL(base_url, item, null, JSON.stringify(termQuery));
            var queryOption = $.get(test, function( data ){
                json_data = JSON.parse(data);
                console.log(searchTerm)
                console.log(json_data);
                for (var obj in json_data) {
                    $select.append($('<option>', {
                        value: obj,
                        text: json_data[obj]["school_name"]
                    }));
                }
            });
        }
    });
}