
class CampaignPageLocators:
    CREATE_CAMP_BUTTON = "//*[text() = 'Создать кампанию']"
    TRAFFIC_BLOCK = '.column-list-item._traffic'
    CAMP_LINK = '[data-gtm-id="ad_url_text"]'
    CAMP_NAME = '.input.input_campaign-name.input_with-close > .input__wrap > .input__inp.js-form-element'
    DAY_BUDGET = '[data-test="budget-per_day"]'
    TOTAL_BUDGET = '[data-test="budget-total"]'
    BANNER_BLOCK = '#patterns_banner_4'

    IMAGE_INPUT = 'input[type="file"][data-test="image_240x400"]'
    CROP_IMAGE_BUTTON = '.image-cropper__save.js-save'
    SUBMIT_BUTTON = '.footer__button.js-save-button-wrap > .button.button_submit[data-class-name="Submit"]'


class LoginPageLocators:
    ENTER_BUTTON = "//*[text() = 'Войти']"
    EMAIL_INPUT = "[name='email']"
    PASSWORD_INPUT = "[name='password']"
    SUBMIT = "div.authForm-module-button-1u2DYF"


class MainPageLocators:
    CAMPAIGN_ICON = '[href="/campaign/new"]'
    SEGMENT_ICON = '[href="/segments"]'


class SegmentsPageLocators:
    CREATE_LINK = '[href="/segments/segments_list/new/"]'
    CREATE_SEGMENT_BUTTON = '.button__text'
    CHECKBOX_PLAYED = '.adding-segments-source__checkbox '
    ADD_SEGMENT_BUTTON = '.adding-segments-modal__btn-wrap  > .button.button_submit  > .button__text'
    SEGMENT_NAME = '.input_create-segment-form .input__wrap > input.input__inp'
    CREATE_SUBMIT_BUTTON = '.create-segment-form__btn-wrap  > .button > .button__text'
    DELETE_SUBMIT_BUTTON = '.button.button_confirm-remove.button_general'
