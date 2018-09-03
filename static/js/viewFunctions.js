function dynamicChoiceGenerator(choice_id, params){
    //dispatch id to the right function
}

function searchSetup(name, item, keyArgs, termArg, helpArg){
    function getURL(baseUrl, item, key, term){
        var paramStr = '?item='+item;
        if(key != null){
            paramStr += '&key='+JSON.stringify(key);
        }
        if(term != null){
            paramStr += '&term='+JSON.stringify(term);
        }
        return baseUrl+paramStr;
    }

    function dynamicRemoveOption(optionFields){
        for(var i = optionFields.options.length-1; i>=0; i--){
            optionFields.remove(i);
        }
    }

    function optionChanged(optionFields, data){
        var i = 0;
        for(obj in data){
            var tempVal = (optionFields[i] ? optionFields[i].value : -1);
            if(tempVal != obj){
                return false;
            }
            i++;
        }
        return (i? true : false);
    }

    function generateHelperText(data, obj, helperArg){
        return (helperArg? ' (' + data[obj][helperArg] + ')' : '');
    }

    var base_url = window.location.origin+"/api/functional/search";
    var initial = true;

    var $select = $('#'+name+"_result");
    var htmlSelect = document.getElementById(name+"_result");
    var $search = $('#'+name+"_search");

    $($search).on("change paste keyup", function() {
        if(initial){
            dynamicRemoveOption(htmlSelect);
            initial = false;
        }
        var searchTerm = $(this).val();
        if (searchTerm.length > 2){
            var termQuery = {};
            termQuery[termArg] = searchTerm;
            var raw_result = getURL(base_url, item, keyArgs, termQuery);
            var queryOption = $.get(raw_result, function( data ){
                json_data = JSON.parse(data);
                if(!optionChanged(htmlSelect, json_data)){
                    dynamicRemoveOption(htmlSelect);
                    for (var obj in json_data) {
                        $select.append($('<option>', {
                            value: obj,
                            text: json_data[obj][termArg] + generateHelperText(json_data, obj, helpArg)
                        }));
                    }
                }
            });
        }else{
            dynamicRemoveOption(htmlSelect);
        }
    });
}