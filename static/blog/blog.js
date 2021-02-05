function update_markdown() {
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", '/post_article/', true);
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.onload = function () {
        var res = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == "200") {
            document.querySelector("#html-markdown").innerHTML = res.html
            console.table(res);
        } else {
            console.error(res);
        }
    }
    data = {}
    data.text = document.querySelector("#markdown").value
    console.log(data)
    json = JSON.stringify(data)
    xhr.send(json);
}

function delete_post(e) {

    var id = e.dataset.id
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/manage_article', true)
    xhr.setRequestHeader('Content-type', 'application/json;charset=utf-8')
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == "200") {
            window.location.href = "/manage_article"
        } else {
            console.error('删除失败')
        }

    }
    var data = {}
    data.id = id
    console.log(data)
    var json = JSON.stringify(data)
    xhr.send(json);

}

// console.log('测试')
// ap1 = new APlayer({
//     container: document.getElementById('aplayer1'),
//     theme: '#e9e9e9',
//     fixed: true,
//     lrcType: 3,
//     audio: [{
//         name: '有何不可',
//         artist: '许嵩',
//         url: 'https://m701.music.126.net/20210205151205/c9f83c8c2dccba3e996f8634aae09bc0/jdyyaac/560e/060b/0009/ad9da805a61acb234e307ce1058b7d4a.m4a',
//         theme: '#ebd0c2'
//     }]
// });
// // cover: 'https://cn-south-17-aplayer-46154810.oss.dogecdn.com/hikarunara.jpg',
//         // lrc: 'https://cn-south-17-aplayer-46154810.oss.dogecdn.com/hikarunara.lrc',