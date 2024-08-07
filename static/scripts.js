function lifeline(options)
{
    for (let element of document.getElementsByClassName("option"))
    {   
        if (options.includes(element.getAttribute("for")))
        {   
            element.style.display = "none";
        }
    }
    document.getElementById('50/50').style.display = "none";

    var http_request = new XMLHttpRequest();
    http_request.open("GET", "/lifeline", true);
    http_request.send();
}

function quiz_submit(ans)
{    
     document.querySelector('[class="option"][for=' + ans + ']').className = "correct-option";

     var options = document.getElementsByName('opt');
     for (let option of options)
     {   
        if (option.checked)
        {   
            var choice = option;
        }
     }

     if (choice.id == ans)
     {
        document.getElementById("correct").style.display = "block";
     }

     else
     {
        document.getElementById("wrong").style.display = "block";
        document.querySelector('[class="option"][for=' + choice.id + ']').className = "wrong-option";
     }
     
     document.getElementById("submit").innerHTML = "Next";
     setTimeout (function() 
     {
        document.getElementById("next").setAttribute("href", window.location.href);
     }, 5);

     var http_request = new XMLHttpRequest();
     http_request.open("GET", "/quiz-submit?ans="+ans+"&choice="+choice.id, true);
     http_request.send();
}

function bookmark(type, classname)
{
    document.querySelector('[class='+classname+'][type='+type).src = "static/bookmark2.png"
    console.log("hi")
}