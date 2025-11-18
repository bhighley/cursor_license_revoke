# Environment Names and Account Numbers (EU vs US)

```mermaid
graph TD
    Title["<b>Environment Names and Account Numbers (EU vs US)</b>"]
    
    Header1["<b>EU Environment Name</b>"]
    Header2["<b>EU Account #</b>"]
    Header3["<b>US Environment Name</b>"]
    Header4["<b>US Account #</b>"]
    
    Title --> Header1
    Title --> Header2
    Title --> Header3
    Title --> Header4
    
    Header1 --> R1C1["Mobile Dev"]
    Header2 --> R1C2["31518660332"]
    Header3 --> R1C3["Mobile Dev"]
    Header4 --> R1C4["31518660332"]
    
    Header1 --> R2C1["EU-INT"]
    Header2 --> R2C2["858308689720"]
    Header3 --> R2C3["Cloud-INT"]
    Header4 --> R2C4["444235492013"]
    
    Header1 --> R3C1["EU-QA"]
    Header2 --> R3C2["568730585496"]
    Header3 --> R3C3["US-QA"]
    Header4 --> R3C4["685815368936"]
    
    Header1 --> R4C1["EU-System Test"]
    Header2 --> R4C2["450234543935"]
    Header3 --> R4C3["US-SystemTest"]
    Header4 --> R4C4["798382343803"]
    
    Header1 --> R5C1["10xPerf"]
    Header2 --> R5C2["516989349834"]
    Header3 --> R5C3["10xPerf"]
    Header4 --> R5C4["516989349834"]
    
    Header1 --> R6C1["EU-Staging"]
    Header2 --> R6C2["761042451864"]
    Header3 --> R6C3["US-Staging"]
    Header4 --> R6C4["761042451864"]
    
    Header1 --> R7C1["EU-Commercial"]
    Header2 --> R7C2["425557308772"]
    Header3 --> R7C3["US-Commercial"]
    Header4 --> R7C4["699069681480"]
    
    Header1 --> R8C1["EU-Clinical"]
    Header2 --> R8C2["576542144457"]
    Header3 --> R8C3["US-Clinical"]
    Header4 --> R8C4["673098177177"]
    
    classDef headerStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef titleStyle fill:#2E5C8A,stroke:#1A3A5A,stroke-width:3px,color:#fff
    classDef dataStyle fill:#E8F4F8,stroke:#4A90E2,stroke-width:1px
    
    class Title titleStyle
    class Header1,Header2,Header3,Header4 headerStyle
    class R1C1,R1C2,R1C3,R1C4,R2C1,R2C2,R2C3,R2C4,R3C1,R3C2,R3C3,R3C4,R4C1,R4C2,R4C3,R4C4,R5C1,R5C2,R5C3,R5C4,R6C1,R6C2,R6C3,R6C4,R7C1,R7C2,R7C3,R7C4,R8C1,R8C2,R8C3,R8C4 dataStyle
```

---

## Alternative 1: Side-by-Side Comparison (LR Flowchart)

```mermaid
graph LR
    subgraph EU["🇪🇺 EU Environments"]
        EU1["Mobile Dev<br/>31518660332"]
        EU2["EU-INT<br/>858308689720"]
        EU3["EU-QA<br/>568730585496"]
        EU4["EU-System Test<br/>450234543935"]
        EU5["10xPerf<br/>516989349834"]
        EU6["EU-Staging<br/>761042451864"]
        EU7["EU-Commercial<br/>425557308772"]
        EU8["EU-Clinical<br/>576542144457"]
    end
    
    subgraph US["🇺🇸 US Environments"]
        US1["Mobile Dev<br/>31518660332"]
        US2["Cloud-INT<br/>444235492013"]
        US3["US-QA<br/>685815368936"]
        US4["US-SystemTest<br/>798382343803"]
        US5["10xPerf<br/>516989349834"]
        US6["US-Staging<br/>761042451864"]
        US7["US-Commercial<br/>699069681480"]
        US8["US-Clinical<br/>673098177177"]
    end
    
    EU1 -.-> US1
    EU2 -.-> US2
    EU3 -.-> US3
    EU4 -.-> US4
    EU5 -.-> US5
    EU6 -.-> US6
    EU7 -.-> US7
    EU8 -.-> US8
    
    classDef euStyle fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    classDef usStyle fill:#E25D4A,stroke:#8A2E2E,stroke-width:2px,color:#fff
    
    class EU1,EU2,EU3,EU4,EU5,EU6,EU7,EU8 euStyle
    class US1,US2,US3,US4,US5,US6,US7,US8 usStyle
```

---

## Alternative 2: Class Diagram

```mermaid
classDiagram
    class EU_Environments {
        +Mobile Dev: 31518660332
        +EU-INT: 858308689720
        +EU-QA: 568730585496
        +EU-System Test: 450234543935
        +10xPerf: 516989349834
        +EU-Staging: 761042451864
        +EU-Commercial: 425557308772
        +EU-Clinical: 576542144457
    }
    
    class US_Environments {
        +Mobile Dev: 31518660332
        +Cloud-INT: 444235492013
        +US-QA: 685815368936
        +US-SystemTest: 798382343803
        +10xPerf: 516989349834
        +US-Staging: 761042451864
        +US-Commercial: 699069681480
        +US-Clinical: 673098177177
    }
    
    EU_Environments <.. US_Environments : Regional Pairing
```

---

## Alternative 3a: Mindmap View with Emoji Differentiation

```mermaid
mindmap
  root((Cloud Environments))
    EU Region
      🔴 DEV Mobile Dev
        31518660332
      🔵 INT EU-INT
        858308689720
      🟡 QA EU-QA
        568730585496
      🟦 TEST EU-System Test
        450234543935
      🟣 PERF 10xPerf
        516989349834
      🟠 STAGE EU-Staging
        761042451864
      🟢 PROD EU-Commercial
        425557308772
      🩷 CLINICAL EU-Clinical
        576542144457
    US Region
      🔴 DEV Mobile Dev
        31518660332
      🔵 INT Cloud-INT
        444235492013
      🟡 QA US-QA
        685815368936
      🟦 TEST US-SystemTest
        798382343803
      🟣 PERF 10xPerf
        516989349834
      🟠 STAGE US-Staging
        761042451864
      🟢 PROD US-Commercial
        699069681480
      🩷 CLINICAL US-Clinical
        673098177177
```

---

## Alternative 3b: Mindmap View with Brackets Differentiation

```mermaid
mindmap
  root((Cloud Environments))
    EU Region
      [DEV] Mobile Dev
        31518660332
      [INT] EU-INT
        858308689720
      [QA] EU-QA
        568730585496
      [TEST] EU-System Test
        450234543935
      [PERF] 10xPerf
        516989349834
      [STAGE] EU-Staging
        761042451864
      [PROD] EU-Commercial
        425557308772
      [CLINICAL] EU-Clinical
        576542144457
    US Region
      [DEV] Mobile Dev
        31518660332
      [INT] Cloud-INT
        444235492013
      [QA] US-QA
        685815368936
      [TEST] US-SystemTest
        798382343803
      [PERF] 10xPerf
        516989349834
      [STAGE] US-Staging
        761042451864
      [PROD] US-Commercial
        699069681480
      [CLINICAL] US-Clinical
        673098177177
```

---

## Alternative 3c: Mindmap View with Symbols

```mermaid
mindmap
  root((Cloud Environments))
    EU Region
      ⚡ DEV | Mobile Dev
        31518660332
      🔄 INT | EU-INT
        858308689720
      ✓ QA | EU-QA
        568730585496
      🧪 TEST | EU-System Test
        450234543935
      🚀 PERF | 10xPerf
        516989349834
      📦 STAGE | EU-Staging
        761042451864
      💼 PROD | EU-Commercial
        425557308772
      🏥 CLINICAL | EU-Clinical
        576542144457
    US Region
      ⚡ DEV | Mobile Dev
        31518660332
      🔄 INT | Cloud-INT
        444235492013
      ✓ QA | US-QA
        685815368936
      🧪 TEST | US-SystemTest
        798382343803
      🚀 PERF | 10xPerf
        516989349834
      📦 STAGE | US-Staging
        761042451864
      💼 PROD | US-Commercial
        699069681480
      🏥 CLINICAL | US-Clinical
        673098177177
```

**Legend:**
- 🔴 / ⚡ **DEV** - Development environment
- 🔵 / 🔄 **INT** - Integration testing
- 🟡 / ✓ **QA** - Quality assurance
- 🟦 / 🧪 **TEST** - System testing
- 🟣 / 🚀 **PERF** - Performance testing
- 🟠 / 📦 **STAGE** - Pre-production staging
- 🟢 / 💼 **PROD** - Commercial production
- 🩷 / 🏥 **CLINICAL** - Clinical production

---

## Alternative 4: Block Diagram (Compact Boxes)

```mermaid
block-beta
    columns 4
    block:EU:2
        columns 2
        EU_Title["EU ENVIRONMENTS"]:2
        EU1["Mobile Dev<br/>31518660332"]
        space
        EU2["EU-INT<br/>858308689720"]
        space
        EU3["EU-QA<br/>568730585496"]
        space
        EU4["EU-System Test<br/>450234543935"]
        space
        EU5["10xPerf<br/>516989349834"]
        space
        EU6["EU-Staging<br/>761042451864"]
        space
        EU7["EU-Commercial<br/>425557308772"]
        space
        EU8["EU-Clinical<br/>576542144457"]
        space
    end
    block:US:2
        columns 2
        US_Title["US ENVIRONMENTS"]:2
        US1["Mobile Dev<br/>31518660332"]
        space
        US2["Cloud-INT<br/>444235492013"]
        space
        US3["US-QA<br/>685815368936"]
        space
        US4["US-SystemTest<br/>798382343803"]
        space
        US5["10xPerf<br/>516989349834"]
        space
        US6["US-Staging<br/>761042451864"]
        space
        US7["US-Commercial<br/>699069681480"]
        space
        US8["US-Clinical<br/>673098177177"]
        space
    end
    
    style EU_Title fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style US_Title fill:#E25D4A,stroke:#8A2E2E,color:#fff
```

---

## Alternative 5: Quadrant Chart (by Environment Type)

```mermaid
quadrantChart
    title Cloud Environments Distribution
    x-axis EU → US
    y-axis Development/Test → Production
    quadrant-1 US Production
    quadrant-2 EU Production
    quadrant-3 EU Dev/Test
    quadrant-4 US Dev/Test
    
    EU-Commercial: [0.2, 0.9]
    US-Commercial: [0.8, 0.9]
    EU-Clinical: [0.15, 0.85]
    US-Clinical: [0.85, 0.85]
    EU-Staging: [0.25, 0.7]
    US-Staging: [0.75, 0.7]
    10xPerf-EU: [0.3, 0.5]
    10xPerf-US: [0.7, 0.5]
    EU-System-Test: [0.2, 0.35]
    US-SystemTest: [0.8, 0.35]
    EU-QA: [0.25, 0.2]
    US-QA: [0.75, 0.2]
    EU-INT: [0.15, 0.1]
    Cloud-INT: [0.85, 0.1]
    Mobile-Dev: [0.5, 0.05]
```

---

## Alternative 6: Simple List Format

```mermaid
graph TD
    Title["Environment Accounts<br/>EU vs US"]
    
    Title --> Env1["1️⃣ Mobile Dev<br/>EU: 31518660332 | US: 31518660332"]
    Title --> Env2["2️⃣ Integration<br/>EU-INT: 858308689720 | Cloud-INT: 444235492013"]
    Title --> Env3["3️⃣ QA<br/>EU-QA: 568730585496 | US-QA: 685815368936"]
    Title --> Env4["4️⃣ System Test<br/>EU: 450234543935 | US: 798382343803"]
    Title --> Env5["5️⃣ 10xPerf<br/>EU: 516989349834 | US: 516989349834"]
    Title --> Env6["6️⃣ Staging<br/>EU: 761042451864 | US: 761042451864"]
    Title --> Env7["7️⃣ Commercial<br/>EU: 425557308772 | US: 699069681480"]
    Title --> Env8["8️⃣ Clinical<br/>EU: 576542144457 | US: 673098177177"]
    
    classDef titleStyle fill:#2E5C8A,stroke:#1A3A5A,stroke-width:3px,color:#fff
    classDef envStyle fill:#E8F4F8,stroke:#4A90E2,stroke-width:2px
    
    class Title titleStyle
    class Env1,Env2,Env3,Env4,Env5,Env6,Env7,Env8 envStyle
```

---

## Standard Table View

| EU Environment Name | EU Account # | US Environment Name | US Account # |
|---------------------|--------------|---------------------|--------------|
| Mobile Dev | 31518660332 | Mobile Dev | 31518660332 |
| EU-INT | 858308689720 | Cloud-INT | 444235492013 |
| EU-QA | 568730585496 | US-QA | 685815368936 |
| EU-System Test | 450234543935 | US-SystemTest | 798382343803 |
| 10xPerf | 516989349834 | 10xPerf | 516989349834 |
| EU-Staging | 761042451864 | US-Staging | 761042451864 |
| EU-Commercial | 425557308772 | US-Commercial | 699069681480 |
| EU-Clinical | 576542144457 | US-Clinical | 673098177177 |
