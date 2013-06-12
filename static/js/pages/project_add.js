$(document).ready(function(){
    var addProject = new AddProject();
    addProject.init();
});

function AddProject()
{
    this.init = function(){
        bindEvent();
    }

    function bindEvent(){
        $(".J_pickTime").datepicker({
            dateFormat:"yy-mm-dd"
        });

        $("#J_submitButton").on("click", function(){
            clickSubmitButton($(this));
        });

        $(".J_timeRow").hover(function(){
            hoverInTimePicker($(this));
        },function(){
            hoverOutTimePicker($(this));
        });

        $(".J_selectMileStone").hover(function(){
            hoverInSelectMileStone($(this));
        },function(){
            hoverOutSelectMileStone($(this));
        });
    }

    function clickSubmitButton(actionItem){
    }

    function hoverInTimePicker(actionItem){
        actionItem.children(".J_operations").removeClass("hide");
    }

    function hoverOutTimePicker(actionItem){
        actionItem.children(".J_operations").addClass("hide");
    }

    function hoverInSelectMileStone(actionItem){
        var selectorHtml = $("#J_selectorTemplate").html();
        actionItem.html(selectorHtml);
    }

    function hoverOutSelectMileStone(actionItem){
        var selector = actionItem.children("select");
        var selectedValue = selector.val();

        var selectedOption = actionItem.find("option:selected");
        console.log(selectedOption);

        var replacedHtml = "<label>"+selectedOption.text()+":</label>";

        console.log(selectedOption);
        actionItem.html(replacedHtml);
    }
}
