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

    if(actionItem.context.dataset['time'] > timestamp){
        warningPopout("等会儿，不急。");
    }else{
        warningPopout("走起~");
    }
}
