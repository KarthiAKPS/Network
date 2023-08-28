var l;
var z;
var k = false;

function likeHandler(id, liked){

    const btn = document.getElementById(`btn_${id}`);
    let cnt = document.getElementById(`count_${id}`).innerHTML;
    cnt = parseInt(cnt);

    document.getElementById(`count_${id}`).innerHTML = '';

    btn.classList.remove('btn-success');
    btn.classList.remove('btn-danger');
    btn.classList.remove('fa-thumbs-up');
    btn.classList.remove('fa-thumbs-down');

    if(liked.indexOf(id)>=0){
         z = true;
    }else{
         z = false;
    }
    if(k == true){
    if(l == true){
        fetch(`/unlike/${id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result)
            cnt = cnt - parseInt('1');
            document.getElementById(`count_${id}`).innerHTML = cnt;
            btn.classList.add('btn-success');
            btn.classList.add('fa-thumbs-up');
            l = false;
            k = true;
        })
    }else{
        fetch(`/like/${id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result)
            cnt = cnt + parseInt('1');
            document.getElementById(`count_${id}`).innerHTML = cnt;
            btn.classList.add('btn-danger');
            btn.classList.add('fa-thumbs-down');
            l = true;
            k = true;
        })
    }}else{
        if(z == true){
            fetch(`/unlike/${id}`)
            .then(response => response.json())
            .then(result => {
                console.log(result)
                cnt = cnt - parseInt('1');
                document.getElementById(`count_${id}`).innerHTML = cnt;
                btn.classList.add('btn-success');
                btn.classList.add('fa-thumbs-up');
                k = true;
                l = false;
            })
        }else{
            fetch(`/like/${id}`)
            .then(response => response.json())
            .then(result => {
                console.log(result)
                cnt = cnt + parseInt('1');
                document.getElementById(`count_${id}`).innerHTML = cnt;
                btn.classList.add('btn-danger');
                btn.classList.add('fa-thumbs-down');
                k = true;
                l = true;
            })}
    }
}

function csrfToken(x){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${x}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function onsave(id){
    const content = document.getElementById(`textarea_${id}`).value;
    const cont = document.getElementById(`content_${id}`);
    console.log(content)
    fetch(`/edit/${id}`, {
        method: 'POST',
        headers: {'Content-type': 'application/json', 'X-CSRFToken':csrfToken("csrftoken")},
        body: JSON.stringify({
            content: content
        })
    }).then(response => response.json())
    .then(result => {
        cont.innerHTML = result.data;
})
}

