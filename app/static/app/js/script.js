$('.plus-cart').click(function(){
//    parent node male div
//    console.log(this.parentNode)
//    3 element parent ma quantity che so index 0 thi start thay  so..
//    console.log(this.parentNode.children[2])

//       means ji button click thay temaa pid che e male
//console.log($(this).attr("pid").toString())
       var id=$(this).attr("pid").toString()

       var qua=this.parentNode.children[2]

       $.ajax({
        type:'GET',
        url:"/pluscart",
        data:{
         prod_id:id
        },
        success:function(data){
//        console.log("data =",data)
             qua.innerText=data.quantity
             document.getElementById("amount").innerText=data.total
             document.getElementById("totalamount").innerText =data.totalamount
        }
       })
})


$('.minus-cart').click(function(){

       var id=$(this).attr("pid").toString()

       var qua=this.parentNode.children[2]

       $.ajax({
        type:'GET',
        url:"/minuscart",
        data:{
         prod_id:id
        },
        success:function(data){
//        console.log("data =",data)
             qua.innerText=data.quantity
             document.getElementById("amount").innerText=data.total
             document.getElementById("totalamount").innerText =data.totalamount
        }
       })
})

$('.remove-cart').click(function(){

       var id=$(this).attr("pid").toString()
//        current element
       var qua=this

       $.ajax({
        type:'GET',
        url:"/removecart",
        data:{
         prod_id:id
        },
        success:function(data){

             document.getElementById("amount").innerText=data.total
             document.getElementById("totalamount").innerText =data.totalamount
//             <div class="row">
//             <div class="col-sm-9">
//             <div>
//              <div class="my-3">
//             aa 4 div remove kare atle akhu card vay jai
             qua.parentNode.parentNode.parentNode.remove()
//             location.reload();
        }
       })
    console.log(qua.parentNode.parentNode.parentNode.remove())
})