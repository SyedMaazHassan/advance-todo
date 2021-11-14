if (my_data.length) {


    var today = my_data[0][1];
    var tomorrow = my_data[1][1];
    var week = my_data[2][1];
    var later = my_data[3][1];

    var $tree_today = $("#tree-today"); 
    var $tree_tomorrow = $("#tree-tomorrow"); 
    var $tree_week = $("#tree-week"); 
    var $tree_later = $("#tree-later"); 

    var ids = {
        'TODAY': "#today-container",
        'TOMORROW': "#tomorrow-container", 
        'THIS WEEK': "#week-container",
        'LATER': "#later-container"
    }

    var $trees = {
        'TODAY': $tree_today,
        'TOMORROW': $tree_tomorrow, 
        'THIS WEEK': $tree_week,
        'LATER': $tree_later
    }

    var data = {
        'TODAY': today,
        'TOMORROW': tomorrow, 
        'THIS WEEK': week,
        'LATER': later
    } 



    if (today.length == 0) {
        $("#today-container").hide();
    }

    if (tomorrow.length == 0) {
        $("#tomorrow-container").hide();
    }

    if (week.length == 0) {
        $("#week-container").hide();
    }

    if (later.length == 0) {
        $("#later-container").hide();
    }

    $(function() {
        for (var key in $trees) {
            if ($trees.hasOwnProperty(key)) {

                $trees[key].tree({
                    data: data[key],
                    dragAndDrop: true,
                    autoOpen: true,
                    closedIcon: $('<i class="material-icons">chevron_right</i>'),
                    openedIcon: $('<i class="material-icons">expand_more</i>'),


                    onCreateLi: function(node, $li, is_selected) {
                
                        // Add 'icon' span before title
                        $li.find(".jqtree-element .jqtree-title").attr("id", `title-${node.id}`);

                        
                        $li.find('.jqtree-element .jqtree-title').css({
                            "width": "80%",
                        });

                        $li.find('.jqtree-element .jqtree-title').css("width", "86%")


                        if (node.status == "DONE") {
                            $li.find('.jqtree-element .jqtree-title').css("text-decoration", "line-through");

                            $li.find('.jqtree-element').prepend(
                                `<div class="text-right" style="width:4%" class="edit">
                                    <i class="material-icons done-icon text-success" data-general-status="${node.general_status}" data-task-id="${node.id}">check_box</i>
                                </div>`
                            );
                            $li.find('.jqtree-element').append(
                                `<div class="text-right" style="width:10%" class="edit">
                                    <span class="task-badge DONE"  data-general-status="${node.general_status}" id="status_22">DONE</span>
                                </div>`
                            );
                        }else{
                            $li.find('.jqtree-element').prepend(
                                `<div class="text-right" style="width:4%" class="edit">
                                    <i class="material-icons done-icon"  data-general-status="${node.general_status}" data-task-id="${node.id}">check_box_outline_blank</i>
                                </div>`
                            );

                            if (node.is_parent) {
                                $li.find('.jqtree-element').append(
                                    `
                                    <i 
                                        data-task-id="${node.id}"
                                        style="height: fit-content;"
                                        data-general-status="${node.general_status}" 
                                        class="material-icons mk-pointer bg-secondary text-white p-0 mr-2 radius-100 subtask-add">add</i>
                                    `
                                );                            
                            }

                            $li.find('.jqtree-element').append(
                                `<div class="text-right" style="width:10%" class="edit">
                                    <span class="task-badge TODO"  data-general-status="${node.general_status}" id="mystatus_${node.id}">TODO</span>
                                </div>`
                            );
                        }

                    
                    },



                    onCanMoveTo: function(moved_node, target_node, position) {

                        if (moved_node.is_parent) {
                            if (position != "inside" && target_node.is_parent == true) {
                                return true;
                            }
                            return false;
                        }
            
                        if (position == "inside") {
                            if (target_node.parent.name) {
                                return false;
                            } else {
                                if(target_node == moved_node.parent || target_node.parent == moved_node.parent){
                                    return true
                                }else{
                                    return false
                                }
                            }

                        }else if (position == "after") {
                            if (target_node.parent.name) {
                                if (target_node.parent == moved_node.parent) {
                                    return true;
                                }else{
                                    return false;
                                }
                            }else{
                                return false;
                            }
                        }
                        
                    }
                });

                $trees[key].on('click', '.subtask-add', function (e) {
                    let task_id = $(e.target).data('task-id');
                    let general_status = $(e.target).data('general-status');

                    // Get the node from the tree
                    var node = $trees[general_status].tree('getNodeById', task_id);

                    if (node) {
                        my_parent_selected = node;
                        $("#sub-task-text").val("");
                        $("#general-status-text").text(node.general_status);
                        $("#short-text").text(node.short_text);
                        $("#sub-task-section").show();
                    }

                });

                $trees[key].on( 'click', '.done-icon', function(e) {
                    // Get the id from the 'node-id' data property

                    let task_id = $(e.target).data('task-id');
                    let general_status = $(e.target).data('general-status');

                    // Get the node from the tree
                    var node = $trees[general_status].tree('getNodeById', task_id);

                    if (node) {
                        // Display the node name
                        $.ajax({
                            url: TOGGLE_TASK_URL,
                            type: "GET",
                            data: {
                                task_id: task_id
                            },
                            success: (response)=>{
                                if (response.status) {
                                    $(e.target).text("check_box");
                                    $(e.target).addClass("text-success");
                                    $(`#title-${task_id}`).css("text-decoration", "line-through");
                                    $(`#mystatus_${task_id}`).attr("class", "task-badge DONE");
                                    $(`#mystatus_${task_id}`).text("DONE");
                                    

                                    if (node.is_parent) {
                                        setTimeout(() => {
                                            $trees[general_status].tree('removeNode', node);

                                            let remaining_today = JSON.parse($trees["TODAY"].tree('toJson'));
                                            let remaining_tomorrow = JSON.parse($trees["TOMORROW"].tree('toJson'));
                                            let remaining_week = JSON.parse($trees["THIS WEEK"].tree('toJson'));
                                            let remaining_later = JSON.parse($trees["LATER"].tree('toJson'));
                                            
                                            if (remaining_today.length == 0) {                                                    
                                                $(ids["TODAY"]).hide();
                                            }

                                            if (remaining_tomorrow.length == 0) {                                                    
                                                $(ids["TOMORROW"]).hide();
                                            }

                                            if (remaining_week.length == 0) {                                                    
                                                $(ids["THIS WEEK"]).hide();
                                            }

                                            if (remaining_later.length == 0) {                                                    
                                                $(ids["LATER"]).hide();
                                            }

                                            if (remaining_today.length == 0 && remaining_tomorrow.length == 0 && remaining_week.length == 0 && remaining_later.length == 0) {
                                                $("#no-task-warning").show()
                                            }

                                        }, 1000);
                                    }
                                }else{
                                    alert(response.message);
                                }
                            }
                        });
                    }
                });

            }
        }


    });



    function reset_child_section() {
        my_parent_selected = null;
        $("#sub-task-text").val("");
        $("#sub-task-section").hide();
    }


    $("#cancel-sub-task").on("click", function () {
        reset_child_section()
    });


  
    // $("#sub-task-submit").on("click", function () {
    //     let new_sub_task = $("#sub-task-text").val();
    //     if (new_sub_task) {
                
    //         $.ajax({
    //             url: CREATE_CHILD_TASK,
    //             type: "GET",
    //             data: {
    //                 my_parent_task: my_parent_selected.id,
    //                 child_task_text: new_sub_task
    //             },
    //             success: (response)=>{

    //                 if (response.status) {

    //                     var parent_node = $trees[my_parent_selected.general_status].tree('getNodeById', my_parent_selected.id);
                        
    //                     $trees[my_parent_selected.general_status].tree(
    //                         'appendNode',
    //                         response.data,
    //                         parent_node
    //                     );
    //                     $trees[my_parent_selected.general_status].tree('openNode', parent_node, false);

    //                     reset_child_section();
                    
    //                 }else{
    //                     alert(response.message);
    //                 }
    //             }
    //         });
            
    //     }
    // })


    // setInterval(() => {
    //     $.ajax({
    //         url: UPDATE_PRIORITY,
    //         type: "GET",
    //         data: {
    //             'my_tree': $my_tree.tree('toJson'),
    //             'today':$trees["TODAY"].tree('toJson'),
    //             'tomorrow':$trees["TOMORROW"].tree('toJson'),
    //             'week':$trees["THIS WEEK"].tree('toJson'),
    //             'later':$trees["LATER"].tree('toJson')
    //         },
    //         success: (response)=>{
    //             if (response.status) {
    //                 console.log(response.message);
    //             }else{
    //                 alert(response.message)
    //             }
    //         }
    //     });
    // }, 4000);


    
}else{
    $("#today-container").hide();
    $("#tomorrow-container").hide();
    $("#week-container").hide();
    $("#later-container").hide();

    $("#no-task-warning").show()
}