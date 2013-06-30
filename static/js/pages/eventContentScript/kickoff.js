(function(){
    var body = $("body");

    body.on("click", "#J_kickOffButton", function(){
        kickOffButtonClicked($(this));
    });
})();

function kickOffButtonClicked(actionItem){
    alert("project id is "+actionItem.context.dataset['projectId']+
          "\ncategory is "+actionItem.context.dataset['category']+
          "\ntimestamp is "+actionItem.context.dataset['time']
        );
}
