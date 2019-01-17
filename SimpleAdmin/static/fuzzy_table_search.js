$(document).ready(function() {
    var activeSystemClass = $('.list-group-item.active');

    //something is entered in search form
    $('#search').keyup( function() {
        var that = this;
        var inputText = $(that).val().toLowerCase();
        // affect all table rows on in systems table
        var tableBody = $('.table tbody');
        var tableRowsClass = $('.table tbody tr');
        
        $('.search-sf').remove();
        tableRowsClass.each( function(i, val) {
            //Lower text for case insensitive
            var name = $(val).find('td')[0].innerHTML.toLowerCase();

            // If row does not contains text, hide it
            if( name.indexOf( inputText ) == -1 )
            {
                tableRowsClass.eq(i).hide();
            }
            else
            {
                tableRowsClass.eq(i).show();
            }
        });
        //all tr elements are hidden
        if(tableRowsClass.children(':visible').length == 0)
        {
            tableBody.append('<tr class="search-sf"><td>No items were found</td></tr>');
        }
    });
});