function deal_error(response){
    if(response.status != 200){
        $("#starter-template").html("<h1>"+response.statusText+"</h1>")
        return true
    }
    data = jQuery.parseJson(response.data)
    if(!data.status){
        $("#starter-template").html("<h1>"+data.error+"</h1>")
        return true
    }
    return false
}

$("#start").click(function(e){
    e.preventDefault();
    var l = Ladda.create(this);
    l.start();
    var params = new URLSearchParams();
    params.append('name',$("#name").val())
    params.append('num',1)
    axios.post("/add",params).then(function(response){
        console.log(response)
        l.stop();
        if(deal_error(response))
            return
        $("#starter-template").html("<p class=\"lead\">第一次录入指纹（共三次）</p>")
        params.set("num",2)
        axios.post("/add",params).then(function(response){
            if(deal_error(response))
                return
            $("#starter-template").html("<p class=\"lead\">第二次录入指纹（共三次）</p>")
            params.set("num",3)
            axios.post("/add",params).then(function(response){
                if(deal_error(response))
                    return
                $("#starter-template").html("<p class=\"lead\">录入完成</p>")
            })
        })
    })
})