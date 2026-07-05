"""Custom ZHA quirk: Tuya/Zemismart 2-gang switch with on/off backlight colour control."""

from zigpy.quirks.v2 import EntityType
import zigpy.types as t

from zhaquirks.tuya.builder import TuyaQuirkBuilder

# --------------------------------------------------------------------------
MANUFACTURER = "_TZE284_7ytnacie"
MODEL = "TS0601"
# --------------------------------------------------------------------------


class IndicatorColour(t.enum8):
    """Preset indicator LED colours."""
    Red = 0x00
    Blue = 0x01
    Green = 0x02
    White = 0x03
    Yellow = 0x04
    Magenta = 0x05
    Cyan = 0x06


class IndicatorMode(t.enum8):
    """Indicator LED operating mode."""
    Relay = 0x00
    None_ = 0x01
    Position = 0x02


class PowerOnBehavior(t.enum8):
    """Relay state after power restoration."""
    Off = 0x00
    On = 0x01
    Memory = 0x02


(
    TuyaQuirkBuilder(MANUFACTURER, MODEL)

    #
    # Relay controls
    #
    .tuya_switch(
        dp_id=1,
        attribute_name="state_l1",
        entity_type=EntityType.STANDARD,
        translation_key="switch_1",
        fallback_name="Switch 1",
    )
    .tuya_switch(
        dp_id=2,
        attribute_name="state_l2",
        entity_type=EntityType.STANDARD,
        translation_key="switch_2",
        fallback_name="Switch 2",
    )
    .tuya_switch(
        dp_id=3,
        attribute_name="state_l2",
        entity_type=EntityType.STANDARD,
        translation_key="switch_2",
        fallback_name="Switch 2",
    )
    .tuya_switch(
        dp_id=4,
        attribute_name="state_l2",
        entity_type=EntityType.STANDARD,
        translation_key="switch_2",
        fallback_name="Switch 2",
    )
    #
    # Master switch
    #
    .tuya_switch(
        dp_id=13,
        attribute_name="master_switch",
        entity_type=EntityType.STANDARD,
        translation_key="master_switch",
        fallback_name="Master switch",
    )

    #
    # Child lock
    #
    .tuya_switch(
        dp_id=101,
        attribute_name="child_lock",
        entity_type=EntityType.CONFIG,
        translation_key="child_lock",
        fallback_name="Child lock",
    )

    #
    # Backlight level
    #
    .tuya_number(
        dp_id=102,
        attribute_name="backlight",
        type=t.uint16_t,
        min_value=0,
        max_value=100,
        step=1,
        entity_type=EntityType.CONFIG,
        translation_key="backlight",
        fallback_name="Backlight level",
    )

    #
    # Enable off-colour indication
    #
    .tuya_switch(
        dp_id=16,
        attribute_name="off_colour_switch",
        entity_type=EntityType.CONFIG,
        translation_key="off_colour_switch",
        fallback_name="Off colour enabled",
    )

    #
    # Indicator colours
    #
    .tuya_enum(
        dp_id=103,
        attribute_name="on_colour",
        enum_class=IndicatorColour,
        entity_type=EntityType.CONFIG,
        translation_key="on_colour",
        fallback_name="On colour",
    )

    .tuya_enum(
        dp_id=104,
        attribute_name="off_colour",
        enum_class=IndicatorColour,
        entity_type=EntityType.CONFIG,
        translation_key="off_colour",
        fallback_name="Off colour",
    )

    #
    # Indicator mode
    #
    .tuya_enum(
        dp_id=15,
        attribute_name="indicator_mode",
        enum_class=IndicatorMode,
        entity_type=EntityType.CONFIG,
        translation_key="indicator_mode",
        fallback_name="Indicator mode",
    )

    #
    # Power-on behaviour
    #
    .tuya_enum(
        dp_id=14,
        attribute_name="power_on_behavior",
        enum_class=PowerOnBehavior,
        entity_type=EntityType.CONFIG,
        translation_key="power_on_behavior",
        fallback_name="Power on behavior",
    )

    .skip_configuration()
    .add_to_registry()
)