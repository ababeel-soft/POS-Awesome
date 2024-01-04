frappe.ui.form.on('Sales Order', {
	bundle_details(frm){
        show_image(frm);
	},
	refresh(frm){

        hide_custom_buttons(frm);
        show_image(frm);
       
	},
	onload(frm){
	}
	
});

function show_image(frm){

        console.log("Stable");
        if (frm.doc.bundle_details){
        let $preview = "";
        frappe.db.get_doc("Item",frm.doc.bundle_details).then((item) => {
        console.log(item.image);
        $preview = $(`<div align="center">
        <img
        class="img-responsive"
        src=${item.image}
        />
        </div>`);
        if ($preview) {
        var html =frm.get_field("custom_image_view").$wrapper.html($preview);
        }
        });
        
        }
}

function hide_custom_buttons(frm){
    setTimeout(() => {
        frm.remove_custom_button('Update Items');
        frm.remove_custom_button('Close', 'Status');
        frm.remove_custom_button('Hold', 'Status');
        frm.remove_custom_button('Work Order', 'Make');
        frm.remove_custom_button('Subscription','Create');
        },10);
}