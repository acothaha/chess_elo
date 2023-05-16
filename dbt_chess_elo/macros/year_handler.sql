{# This macro will handle the year column if there is error #}

{% macro year_handler(year) %}

    case
        when SAFE_CAST({{ year }} as integer) is NULL then CAST(EXTRACT(year from CURRENT_DATE()) AS smallint)
        else CAST({{ year }} AS smallint)
    end

{% endmacro %}