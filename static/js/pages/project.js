$(document).ready(function(){
    var project = new Project();
    project.init();
});

function Project(){
    this.init = function(){
        bindEvent();
    };

    function bindEvent(){
        $(".J_operationButton").on("click", function(){
            operationButtonClicked($(this));
        });
    }

    function operationButtonClicked(actionItem){
        var data_id = actionItem.attr("data-id");
        window.location.href="/timeline?id="+data_id;
    }
}
