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

        $(".J_deleteButton").on("click", function(){
            deleteButtonClicked($(this));
        });
    }

    function operationButtonClicked(actionItem){
        var data_id = actionItem.attr("data-id");
        window.location.href="/timeline?id="+data_id;
    }

    function deleteButtonClicked(actionItem){
        var projectId = actionItem[0].dataset.id;
        var data = {
            "projectId":projectId
        };
        var paramString = $.toJSON(data);
        $.post("/project/del", {data:paramString}, function(result){
            location.reload();
        }, "json");
    }
}
