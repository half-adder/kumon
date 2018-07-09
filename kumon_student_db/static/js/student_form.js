$("document").ready(function() {

    // Relevant elements
    // Auto-generated elements
    let startDate = $('#id_start_date');
    let mathLevel = $('#id_math_level');
    let readingLevel = $('#id_reading_level');
    let regDiscount = $('#id_registration_discount_percent');
    let regCost = $('#registration_cost');

    // Cost Table Elements
    let mathProratedCost = $('#math_prorated_cost');
    let readingProratedCost = $('#reading_prorated_cost');
    let mathMonthlyCost = $('.math-monthly-cost');
    let readingMonthlyCost = $('.reading-monthly-cost');
    let totalCost = $('#total_cost');

    updateCosts();
    $(document).on("change keyup", '.cost-input', updateCosts);

    function updateCosts() {
        console.log("hello");

        let startDateText = getStartDateText();
        let nSubjects = getSubjectCount();
        let regDiscountInt = getRegDiscount();

        getCostInfo(startDateText, nSubjects, regDiscountInt, setCostInfo);
    }

    function getStartDateText() {
        return startDate.val();
    }

    function getSubjectCount() {
        let subjectCount = 0;
        if (mathLevel.val()) {
            subjectCount += 1;
        }
        if (readingLevel.val()) {
            subjectCount += 1;
        }
        return subjectCount;
    }

    function getRegDiscount() {
        return parseInt(regDiscount.val());
    }


    function setCostInfo(costInfo) {
        regCost.text(costInfo['registration_cost']);
        totalCost.text(costInfo['total_cost']);

        // Math Cost Info
        if (mathLevel.val()) {
            mathMonthlyCost.text(costInfo['monthly_cost']);
            mathProratedCost.text(costInfo['prorated_cost']);
        } else {
            mathMonthlyCost.text(0);
            mathProratedCost.text(0);
        }

        // Reading Cost Info
        if (readingLevel.val()) {
            readingMonthlyCost.text(costInfo['monthly_cost']);
            readingProratedCost.text(costInfo['prorated_cost']);
        } else {
            readingMonthlyCost.text(0);
            readingProratedCost.text(0);
        }
    }
});


function getCostInfo(startDate, nSubjects, regDiscount, callback) {
    const params = {
        'start_date': startDate,
        'n_subjects': nSubjects,
        'registration_discount': regDiscount
    };
    let url = costInfoURL + $.param(params);

    $.ajax({
        type: 'GET',
        url: url,
        success: callback,
    });
}
