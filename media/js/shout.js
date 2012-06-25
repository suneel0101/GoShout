$(document).ready(function(){
    insertTimeChoices();
});


function insertTimeChoices(){
    alert('1');
    var d=new Date();
    var hours=parseInt(d.getHours());
    var minutes=d.getMinutes();
    var dutc=new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), d.getUTCHours(), d.getUTCMinutes());
    var utcyear=dutc.getFullYear();
    var utcmonth=dutc.getMonth();
    var utcdate=dutc.getDate();
    var utchour=dutc.getHours();
    var utcminute=dutc.getMinutes();
    $("#event_time_field").empty();
    var now_time_string=dutc.getDate()+":"+dutc.toTimeString();
    var html='<option selected="selected" value="'+now_time_string+'">Now</option>';
    //round utc time to 15s;
    dutc.setMinutes(roundUTCTime(dutc));
    for(i=0; i<96; i++){
        dutc.setMinutes ( dutc.getMinutes() + 15 );
        minutes=howManyMinutes(minutes);
        if(minutes=="00"){
            hours++;
        }
        if(hours>23){
            hours=0;
        }
        var am_pm="am";
        if(hours>12){
            am_pm="pm"
        }
        var time_string=dutc.getDate()+":"+dutc.toTimeString();
        html+='<option value="'+time_string+'">'+adjustHours(hours)+':'+minutes+am_pm+'</option>';
    }
    $("#event_time_field").append(html);


}

function roundUTCTime(utc){
    var minutes=parseInt(utc.getMinutes());
    var setmin;
    if(minutes<15){
        setmin=0;
    }
    else if(minutes<30){
        setmin=15;
    }
    else if(minutes<45){
        setmin=30;
    }
    else{
        setmin=45;
    }
    return setmin;
}

function howManyMinutes(m){
    var n=parseInt(m);
    var min="";
    if(n>=0 && n<15){
        min="15";
    }
    else if(n>=15 && n<30){
        min="30";
    }
    else if(n>=30 && n<45){
        min="45";
    }
    else{
        min="00";
    }
    return min;
}

function adjustHours(h){
    var hours=parseInt(h);
    if(hours>12){
        hours-=12;
    }
    else if(hours==0){
        hours=12;
    }
    return hours;
}

function minutesString(m){
    var min="";
    if(m<10){
        min="0"+m;
    }
    else{
        min=m.toString();
    }
    return min;
}