# Finite Number Points and 32-Item Small Baskets

Previous stop: [Two Frames and Reset](L1_00_history_primer.md) · Next stop: [L1.01 Pre-Graph Preparation](L1_01_prepare.md) · [Back to Index](INDEX.md)

Optional drill-down: [Exact 32-Item Rules](L3_qmma_e4m3.md) · [Numeric Glossary Entries](APPENDIX_beginner_glossary.md#g054)

Fractional numbers stored by a machine can land only on specific number points. [F16](APPENDIX_beginner_glossary.md#g054) uses 16 binary bits and [E4M3](APPENDIX_beginner_glossary.md#g055) uses 8 bits to store a number; neither retains 16 or 8 decimal places. The spacing between actual number points varies with magnitude; the evenly spaced ruler below is for **synthetic teaching** only.

~~~text
Synthetic ruler:  −2  ·  −1.5  ·  −1  ·  −0.5  ·  0  ·  0.5  ·  1  ·  1.5  ·  2
Value 1.75 to store: nearest points are 1.5 and 2 (exact midpoint); the illustrated even tie-break chooses 2.
Toward zero: 1.75 takes 1.5; −1.75 takes −1.5. Floor rounding pushes negative numbers more negative and must not be confused with this.
~~~

"Round to nearest-even" first finds the nearest **representable value**, checking whether the least significant bit of the [encoded](APPENDIX_beginner_glossary.md#g057) [significand](APPENDIX_beginner_glossary.md#g058) is 0 only on an exact midpoint tie; it does not round arbitrary fractions to even integers. Actual F16 example: 1 and 1+2⁻¹⁰ are adjacent, and their midpoint 1+2⁻¹¹ is saved as 1. [RZ](APPENDIX_beginner_glossary.md#g060) is round toward zero, and [RN16](APPENDIX_beginner_glossary.md#g059)/RN32/RN64 are round-to-nearest-even to different bit widths. Tiny numbers may be rounded away; certain operations also actively flush [subnormal](APPENDIX_beginner_glossary.md#g068) numbers to zero (FTZ), which cannot be applied across the board to all sites.

<a id="baskets"></a>
## One Row Times One Column: Processing 64 Pairs of Numbers in Two Baskets

Multiplying each pair and adding up the products is called a [dot product](APPENDIX_beginner_glossary.md#g051). Here one basket processes 32 pairs and brings in a saved subtotal; the first basket can start from 0 or from a specified [bypass](APPENDIX_beginner_glossary.md#g016).

~~~mermaid
flowchart LR
    A["First 32 product pairs + starting subtotal"] --> G["Place each toward zero onto the same common scale"] --> S["Add the 32 items and subtotal exactly on that scale"] --> H["Save F16 subtotal via round-to-nearest-even"]
    H --> B["Bring into next basket with remaining 32 pairs"] --> G2["Reselect common scale, place each, and add"] --> H2["Save F16 again"]
    H2 --> Q["If required by this exit: separately convert to E4M3"]
~~~

A "[common scale](APPENDIX_beginner_glossary.md#g066)" acts like a shared fine ruler on which the products and subtotal in the same basket are first placed at a uniform grid step, truncating any unrepresentable tail toward zero. The ruler is selected jointly from the exponents in the operand encodings and the incoming subtotal; for the exact scale-selection formula, see the [expert rules](L4_e4m3_and_k32.md#qmma-k32-accumulation). Thus saving F16 only once at the end of the step **does not mean no precision was lost before that point**. Neither is each product converted to F16 immediately, nor are all 64 pairs summed before converting once.

<a id="reuse-examples"></a>
| Reused synthetic examples, none a measurement | What it shows |
|---|---|
| [A: 1, 2⁻¹¹, 2⁻¹⁸](L4_e4m3_and_k32.md#worked-examples) | In the same basket the three items end up at 1+2⁻¹⁰; saving the first two items first and putting the third in the next basket yields 1. Basket boundaries change rounding |
| Same page B: 256, −256, 2⁻¹⁸ | Common grid step 2⁻¹⁷ truncates the last item to 0 first, giving sum 0; one cannot perform real-number [cancellation](APPENDIX_beginner_glossary.md#g071) first and keep the tiny tail |
| Same page C: 1+2⁻⁴+2⁻¹⁸ | Saving F16 first yields 1.0625, and then converting to E4M3 yields 1; converting directly to E4M3 would yield 1.125. Two conversions do not equal one |

<a id="three-cards"></a>
## Carry Three Check Cards with You

| Card | Question to ask |
|---|---|
| What the format can represent | Does this number have a corresponding storage code? Even within the same format, number points are not evenly spaced; [+0](APPENDIX_beginner_glossary.md#g070) and −0 have distinct encodings |
| How this operation computes | Where does it truncate to a common grid, round, flush to zero, or convert? Ordinary add/multiply, [fused multiply-add](APPENDIX_beginner_glossary.md#g063), 32-item steps, 16-item steps, and final color each have their own rules |
| What the current implementation allows | Representable does not mean permitted as input; [NaN](APPENDIX_beginner_glossary.md#g069)/Inf, overflow, and other guards may reject, and a rejection produces no output that can be counted as a match |

This page explains the 32-item E4 software reproduction rule on the target [sm_120](APPENDIX_beginner_glossary.md#g078) and its existing finite-domain evidence. It does not prove that physical baskets or rulers exist inside the device, does not prove behavior across all inputs or future devices, and does not cover the separate 16-item steps, [texture](APPENDIX_beginner_glossary.md#g027) sampling, or final color conversion. The [per-operation rounding table](L4_half_arith.md#beginner-rounding) preserves those distinctions, and the [full boundaries](L3_qmma_e4m3.md#候选如何从-1832-收敛到一个行为类) remain in effect.
