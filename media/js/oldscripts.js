var prefix="";
$(document).ready(function(){
    insertTimeChoices();
    bindNewEventButton();
});

$(document).on('click', '#log_out_button', function(){
    window.location.href="/logout/";
});


$(document).delegate("#feed", "pagecreate", function(){
    //getEvents();
});

function bindNewEventButton(){
    $(document).on('click', '#shout_new_event_button', function(){
        insertTimeChoices();
        refreshShoutForm();
    });
}

function bindSubmitEventButton(){
/*    $(document).on('click', '#event_submit_button', function(){
        refreshShoutForm();
    });*/
}

/* code for ajax submit
function submitEventCreation(){
    var $selected=$("select option:selected");
    var year=$selected.data("year");
    var month=$selected.data("month");
    var date=$selected.data("date");
    var hour=$selected.data("hour");
    var minute=$selected.data("minute");
    var location=$("#event_location_field").val();
    var name=$("#event_name_field").val();
    var e_obj=new Object();
    e_obj.year=year;
    e_obj.month=month;
    e_obj.date=date;
    e_obj.hour=hour;
    e_obj.minute=minute;
    e_obj.location=location;
    e_obj.name=name;
    $.post(
        prefix+'/create/',
        e_obj
    ).done(function(data){
        getEvents();
    });
}*/

function getEvents(){
    $.get(
        prefix+'/events/'
    ).done(function(data){
        appendFeedData(data);
    });
}

function appendFeedData(data){
        $("#invite_list_ul").empty();
        var data_length=data.length;
        var append_html='';
        for(i=0; i<data_length; i++){
            var year=data[i].year;
            var month=data[i].month;
            var date=data[i].day;
            var hour=data[i].hour;
            var minute=data[i].minute;
            var d=new Date(year, month, date, hour, minute);
            var ds=new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()-1, d.getUTCHours(), d.getUTCMinutes());
            var local_hours=ds.getHours();
            var am_pm="am";
            if(local_hours>12){
                am_pm="pm"
            }
            var time_string=adjustHours(local_hours)+":"+minutesString(ds.getMinutes())+am_pm;
            //append_html+='<li><a href="#">hello</a></li>';
            append_html+='<li><a href="#"><p class="ui-li-aside ui-li-desc"><strong>'+data[i].reshout_count+' Reshouts!</strong></p><h3 class="ui-li-heading">'+data[i].name+'</h3><p class="ui-li-desc">Created by: <strong>'+data[i].host+'</strong></p><p class="ui-li-desc">in '+data[i].location+' @ <strong>'+time_string+'</strong></p></a></li>';
        }
        $("#invite_list_ul").append(append_html).trigger('create');
}

function insertTimeChoices(){
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
    var html='<option value="'+now_time_string+'">Now</option>';
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
    $("#event_time_field").append(html).trigger('create');
    $(".ui-select").find("span .ui-btn-text").html("Now");


}

function refreshShoutForm(){
    $("#event_name_field").val("");
    $("#event_location_field").val("");
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