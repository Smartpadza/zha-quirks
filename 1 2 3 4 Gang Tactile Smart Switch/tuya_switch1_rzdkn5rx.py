"""Custom ZHA quirk: Tuya/Zemismart 1-gang switch with on/off backlight colour control."""
 
from zigpy.quirks.v2 import EntityType
import zigpy.types as t
 
from zhaquirks.tuya.builder import TuyaQuirkBuilder
 
# --- EDIT THESE TWO VALUES --------------------------------------------------
MANUFACTURER = "_TZE284_rzdkn5rx"  # from "Zigbee Device Signature" in ZHA
MODEL = "TS0601"
# -----------------------------------------------------------------------------
 
 
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
    """How the indicator LED tracks relay state."""
    Relay = 0x00  # LED follows relay state (uses on_colour / off_colour)
    none = 0x01  # LED always off
    pos = 0x02  # LED shows position/some other fixed behaviour
 
 
class PowerOnBehavior(t.enum8):
    """Relay state to restore to after a power loss."""
    Off = 0x00
    On = 0x01
    Memory = 0x02
 
 
(
    TuyaQuirkBuilder(MANUFACTURER, MODEL)
    # Main relay / on-off control.
    .tuya_switch(
        dp_id=1,
        attribute_name="on_off",
        entity_type=EntityType.STANDARD,
        translation_key="on_off",
        fallback_name="Switch",
    )
    # Separate "master" switch present on some variants of this device.
    .tuya_switch(
        dp_id=13,
        attribute_name="master_switch",
        entity_type=EntityType.STANDARD,
        translation_key="master_switch",
        fallback_name="Master switch",
    )
    .tuya_switch(
        dp_id=101,
        attribute_name="child_lock",
        entity_type=EntityType.CONFIG,
        translation_key="child_lock",
        fallback_name="Child lock",
    )
    # Indicator LED brightness/level. See note above re: max_value.
    .tuya_number(
        dp_id=102,
        attribute_name="backlight_level",
        type=t.uint16_t,
        min_value=0,
        max_value=100,
        step=1,
        entity_type=EntityType.CONFIG,
        translation_key="backlight_level",
        fallback_name="Backlight level",
    )
    # Enables/disables the "off colour" indicator behaviour.
    .tuya_switch(
        dp_id=16,
        attribute_name="off_colour_switch",
        entity_type=EntityType.CONFIG,
        translation_key="off_colour_switch",
        fallback_name="Off colour enabled",
    )
    # Colour shown by the indicator LED while the relay/switch is ON.
    .tuya_enum(
        dp_id=103,
        attribute_name="on_colour",
        enum_class=IndicatorColour,
        entity_type=EntityType.CONFIG,
        translation_key="on_colour",
        fallback_name="On colour",
    )
    # Colour shown by the indicator LED while the relay/switch is OFF.
    .tuya_enum(
        dp_id=104,
        attribute_name="off_colour",
        enum_class=IndicatorColour,
        entity_type=EntityType.CONFIG,
        translation_key="off_colour",
        fallback_name="Off colour",
    )
    # Overall indicator mode: follow relay state, always off, or "pos".
    .tuya_enum(
        dp_id=15,
        attribute_name="indicator_mode",
        enum_class=IndicatorMode,
        entity_type=EntityType.CONFIG,
        translation_key="indicator_mode",
        fallback_name="Indicator mode",
    )
    # Relay state restored after a power loss.
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