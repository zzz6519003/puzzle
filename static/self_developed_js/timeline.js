$(document).ready(function(){
    timeline = new TimeLine();
    timeline.init();
});

function TimeLine()
{
    this.init = function(){
        generateTimeLine();
        bindEvent();
    };

    function bindEvent(){
    }

    function generateTimeLine(){
       //createStoryJS({
       //    type:"timeline",
       //    width:"1280",
       //    height:"800",
       //    source:"static/example_json.json",
       //    embed_id:"J_timeline",
       //    debug:false
       //}); 
    }
}
