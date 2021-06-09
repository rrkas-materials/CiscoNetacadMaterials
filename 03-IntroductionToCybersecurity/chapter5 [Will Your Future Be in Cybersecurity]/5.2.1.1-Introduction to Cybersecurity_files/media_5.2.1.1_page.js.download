function registerSWF() {
    swfobject.registerObject("flashobject", "9.0.0", "../../../common/libs/expressInstall.swf");
}

loadScript("../../../common/scripts/swfobject.js", registerSWF);

(slideViewDidLoad = function(_container, _id) {
    btnXPosArr = [320, 709.9, 709.9];
    btnYPosArr = [250, 170, 350];
    buttonArr = [];
    buttonClickArr = [];
    buttonOverArr = [];
    bubbleArr = [];
    sampleArray = [];
    var lastBtnClick;
    bubbleTitleArr = ["ID_titleTxt01", "ID_titleTxt02", "ID_titleTxt03"]
    bubbleTextArr = ["ID_bodyTxt01", "ID_bodyTxt02", "ID_bodyTxt03"]
    for (var i = 0; i < 3; i++) {
        var container = new createjs.Container()
        _container.addChild(container);
        container.id = i;

        container.cursor = "pointer";


        btn = getCJSElement("IMAGE", { x: btnXPosArr[i], y: btnYPosArr[i], width: 50, height: 50, src: "plus-icon.png", });

        buttonArr.push(btn);
        container.addChild(btn);

        btn1 = getCJSElement("IMAGE", { x: btnXPosArr[i], y: btnYPosArr[i], width: 50, height: 50, src: "plus-icon.png", });

        buttonOverArr.push(btn1);
        container.addChild(btn1);
        btn1.visible = false;

        btn4 = getCJSElement("IMAGE", { x: btnXPosArr[i], y: btnYPosArr[i], width: 50, height: 50, src: "plus-icon.png", });

        buttonClickArr.push(btn4);
        container.addChild(btn4);
        btn4.visible = false;

        container.addEventListener("click", handlerMethod);
        container.addEventListener("mouseover", handlerOverMethod);
        container.addEventListener("mouseout", handlerOutMethod);
        var btn2 = getCJSElement("TEXTBOX", { subType: "CLOSABLE", x: 250, y: 200, width: 500, height: 200, titleId: bubbleTitleArr[i], bodyId: bubbleTextArr[i] });
        _container.addChild(btn2);
        bubbleArr[i] = btn2;
        bubbleArr[i].visible = false;
        bubbleArr[0].visible = false;
        buttonClickArr[0].visible = false;

        //accessibility fix -------------------------------------
        j = i + 1;
        var label = document.createElement("button");
        label.style.cssText = "border: 1px solid rgba(0,0,0,0);padding: 0;background-color:transparent;top:2px;left:2px;cursor:pointer;pointer-events:none;";
        label.innerHTML = "";
        label.id = "btn" + j;
        label.name = "more info";
        label.tabIndex = 0;
        $(label).insertBefore($('#textBoxDiv_' + j));

        $("#btn" + j).attr("aria-label", "More information");
        $("#btn" + j).on("focus", mouseOverFunc);
        $("#btn" + j).on("focusout", mouseOutFunc);
        $("#btn" + j).on("click", clickFunction);
        $("#btn" + j).css({ "position": "absolute", "margin-top": btnYPosArr[i], "margin-left": btnXPosArr[i], "width": 45 + "px", "height": 45 + "px" });


        function mouseOverFunc(event) {
            var id = (event.target.id.split('btn')[1]) - 1;
            buttonOverArr[id].visible = true;
        }

        function mouseOutFunc() {
            var id = (event.target.id.split('btn')[1]) - 1;
            buttonOverArr[id].visible = false;
        }

        function clickFunction(event) {
            var id = (event.target.id.split('btn')[1]) - 1;
            //console.log(event.target.id.split('btn')[1])
            for (i = 0; i < 3; i++) {
                bubbleArr[i].visible = false;
                buttonClickArr[i].visible = false;

            }

            bubbleArr[id].visible = true;
            buttonClickArr[id].visible = true;

        }
        //accessibility fix end-------------

    }


    function handlerMethod(event) {

        for (var i = 0; i < 3; i++) {

            bubbleArr[i].visible = false;
            buttonClickArr[i].visible = false;

        }
        if (lastBtnClick) {
            buttonOverArr[lastBtnClick.id].visible = true;
            lastBtnClick.addEventListener("mouseover", handlerOverMethod);
            lastBtnClick.addEventListener("mouseout", handlerOutMethod);
        }
        bubbleArr[event.target.id].visible = true;
        buttonClickArr[event.target.id].visible = true;

        event.target.removeEventListener("mouseover", handlerOverMethod);
        event.target.removeEventListener("mouseout", handlerOutMethod);
        lastBtnClick = event.target;

    }


    function handlerOverMethod(event) {

        buttonOverArr[event.target.id].visible = true;


    }

    function handlerOutMethod(event) {
        buttonOverArr[event.target.id].visible = false;
    }


});