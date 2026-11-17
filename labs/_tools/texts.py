"""The Arabic texts and the prepared notebooks of the Dhilal file pack. Imported by prepare_files.py.

The six "AI answers", the draft commentary and the prose sample are scripted stand-ins written
by the course author: no language model produced them. Each carries the kind of fault a real
assistant makes, and the figures inside curly braces are filled in by the generator.
"""

ANSWERS = {
"A1.txt": """
الإجابة 1 · السؤال: ما إجمالي إيرادات أكتوبر 2026؟
(رد مكتوب باليد يمثّل مساعدًا يشغّل الرموز البرمجية؛ لم ينتجه نموذج)

شغّلت الرموز الآتية على الملف المرفوع trial_balance_oct.csv:

    import pandas as pd
    tb = pd.read_csv("trial_balance_oct.csv")
    rev = tb[tb["group"] == "إيرادات"]
    print(len(rev), rev["oct_2026"].sum())

المخرج:

    3 {REV}

إجمالي إيرادات أكتوبر {REV} ريال، من 3 حسابات.
""",
"A2.txt": """
الإجابة 2 · السؤال: ما إجمالي مصروفات أكتوبر 2026؟
(رد مكتوب باليد يمثّل مساعد محادثة لا يشغّل رموزًا؛ لم ينتجه نموذج)

راجعت ميزان المراجعة الذي لصقته. حسابات المصروفات أربعة عشر حسابًا، من الرواتب والأجور إلى
استهلاك الأصول. بجمع أرصدة أكتوبر لهذه الحسابات يكون إجمالي المصروفات {A2} ريال.

الرواتب والبدلات والتأمينات هي الجزء الأكبر من هذا الإجمالي، تليها قطع الغيار ومواد النظافة.
""",
"A3.txt": """
الإجابة 3 · السؤال: كم تغيّر حساب الرواتب والأجور عن سبتمبر؟
(رد مكتوب باليد يمثّل مساعدًا داخل جدول البيانات؛ لم ينتجه نموذج)

في ورقة ميزان المراجعة، حساب 5010 «رواتب وأجور» في الصف 5: رصيد سبتمبر في D5 ورصيد أكتوبر في E5.
وضعت في الخلية G5 الصيغة:

    =(E5-D5)/D5

والخلية تعرض الآن {SALPCT}%. إذا تغيّر أي من الرصيدين تغيّرت النسبة معه.
""",
"A4.txt": """
الإجابة 4 · السؤال: ما أكبر حساب مصروفات في أكتوبر، وكم نسبته من إجمالي المصروفات؟
(رد مكتوب باليد يمثّل مساعد محادثة لا يشغّل رموزًا؛ لم ينتجه نموذج)

أكبر حساب مصروفات في أكتوبر هو «{LARGEST}»، ويمثّل نحو {SHARE}% من إجمالي المصروفات.
وهذا متوقع في شركة خدمات مرافق تعتمد على العمالة.
""",
"A5.txt": """
الإجابة 5 · السؤال: كم بندًا من مشتريات العهدة العشرين يُصنَّف «مواد نظافة»؟
(مخرج مكتوب باليد يمثّل دالة ذكاء اصطناعي داخل خلايا الجدول؛ لم ينتجه نموذج)

في العمود C دالة ذكاء اصطناعي تصنّف وصف كل بند في العمود B إلى واحدة من ثلاث فئات.
في العمود كما هو الآن: «مواد نظافة» عددها {C1} من 20.

الملف A5_ai_function_runs.csv فيه العمود نفسه كما ظهر في تحديثين متتاليين للدالة، دون أي تغيير
في الأوصاف.
""",
"A6.txt": """
الإجابة 6 · السؤال: ما إجمالي مصروفات أكتوبر دون تكاليف العاملين (الرواتب والبدلات والتأمينات)؟
(رد مكتوب باليد يمثّل مساعدًا يشغّل الرموز البرمجية؛ لم ينتجه نموذج)

شغّلت الرموز الآتية على الملف المرفوع trial_balance_oct.csv:

    import pandas as pd
    tb = pd.read_csv("trial_balance_oct.csv")
    exp = tb[tb["group"] == "مصروفات"]
    other = exp[~exp["account_name"].str.contains("رواتب")]
    print(len(other), other["oct_2026"].sum())

المخرج:

    {N6} {A6}

إجمالي المصروفات دون تكاليف العاملين {A6} ريال.
""",
}

TEXT_FILES = {
"prework_guide.txt": """
العمل التحضيري قبل اليوم الأول · خط الأساس (نحو 45 دقيقة)
مقرر USE-PRO-203 · الذكاء الاصطناعي في أعمال المالية والمحاسبة والتدقيق

لماذا: في آخر الورشة تعيد تصميم مهمة متكررة واحدة من عملك وتقيس الوقت والأخطاء قبل وبعد.
«قبل» يُقاس الآن، بالطريقة التي تعمل بها اليوم، ودون أي مساعد ذكاء اصطناعي.

1. اختر مهمة مالية أو تدقيقية تتكرر أسبوعيًا أو شهريًا، يأخذ تنفيذها بين 20 و60 دقيقة، ولها ناتج
   يمكن التحقق منه برقم: مطابقة كشف مورد، مطابقة عهدة، تقرير أعمار ذمم، مراجعة عينة مصروفات.
2. نفّذها مرة واحدة كما تفعل دائمًا. سجّل وقت البدء ووقت الانتهاء بالدقائق.
3. اطلب من زميل أن يراجع الناتج، أو راجعه أنت في اليوم التالي مقابل المصدر. عُدّ الأخطاء: فرق
   فاتك، أو فرق أشرت إليه وليس فرقًا، أو رقم نُقل خطأ.
4. املأ سطرًا في redesign/measurement_table.csv: الطريقة «يدوي»، والدقائق، وعدد الأخطاء.
   إن كان عندك سجل تنفيذين سابقين فأضفهما: ثلاثة أسطر أفضل من سطر.
5. اكتب ثلاث جمل: ما مدخلات المهمة؟ ما الرقم الذي يثبت أن ناتجها صحيح؟ ما تصنيف بياناتها؟

لا تُحضر بيانات حقيقية إلى الورشة: أحضر السطر والجمل الثلاث فقط.
من لا مهمة عنده، أو لا يستطيع القياس: يستخدم مهمة شركة ظِلال، مطابقة كشف مورد، وخط أساسها في
redesign/baseline_log_dhilal.csv.
""",
"budget_spec.txt": """
مواصفة نموذج موازنة 2027 · شركة ظِلال لإدارة المرافق (جهة افتراضية)
كتبها شاهين اللهيب، محلل الموازنة، واعتمدتها ثريا الحمداني، المراقبة المالية.

لكل مركز تكلفة من المراكز الاثني عشر:

1. الراتب الشهري الشامل: من جدول الدرجات في ورقة Rates، عمود «الراتب الشهري الشامل (مع البدلات)»،
   حسب الدرجة الغالبة في المركز.
2. الرواتب السنوية 2027 = عدد الموظفين × الراتب الشهري الشامل × 12 × (1 + زيادة الرواتب السنوية).
3. اشتراكات صاحب العمل = الرواتب السنوية 2027 × نسبة الاشتراكات والتأمينات. النسبة واحدة لكل المراكز.
4. مواد وخدمات 2027 = مواد وخدمات 2026 × (1 + تضخم عقود المواد والخدمات).
5. إجمالي موازنة المركز = الرواتب السنوية + الاشتراكات + مواد وخدمات 2027 − المبالغ المستردة من العملاء.

إجمالي موازنة الشركة = مجموع إجماليات المراكز الاثني عشر كلها، ويساوي مجموع القطاعات الأربعة.

الافتراضات في ورقة Assumptions: زيادة الرواتب 4%، الاشتراكات والتأمينات 12%، تضخم العقود 3%.
النسب افتراضات تدريبية لشركة افتراضية، وليست نسبًا نظامية.

الحالات المحسوبة يدويًا: CC-101 وCC-105 وCC-112، ثم إجمالي الشركة. املأها في hand_cases.csv
بآلة حاسبة ودون مساعد، قبل أن تنظر إلى أرقام النموذج.
""",
"cc_notes.txt": """
ملاحظات أصحاب مراكز التكلفة على مصروفات أكتوبر 2026 · شركة ظِلال (بيانات اصطناعية)
جمعها شاهين اللهيب حتى 3 نوفمبر 2026. ما ليس هنا لم يصل عنه شيء.

CC-104 الصيانة الميدانية · زهور الشبل:
  عمل إضافي لفريقين مدة تسعة أيام بعد تعطل التكييف المركزي في مبنى عميل. أوامر العمل WO-2610-118
  إلى WO-2610-131. العميل وافق كتابةً على تحميله 60% من التكلفة في فاتورة نوفمبر.

CC-107 الحراسات الأمنية · مدير القطاع:
  بدأ عقد حراسة جديد في 12 أكتوبر (العقد SEC-2026-044) بثمانية حراس إضافيين. إيراد العقد يبدأ
  في أكتوبر أيضًا، ولم يكن في الموازنة.

CC-110 أسطول المركبات · مدير الأسطول:
  تأجل استلام مركبتين مستأجرتين إلى نوفمبر (مذكرة FLT-M-031). الوفر مؤقت وسيظهر مصروفًا في نوفمبر.

لا ملاحظات من: CC-102 نظافة المجمعات التجارية، ولا من CC-109 المشتريات والمستودعات.
""",
"ai_draft_commentary.txt": """
مسودة تعليق الانحرافات · أكتوبر 2026
(مسودة مكتوبة باليد تمثّل ما يكتبه مساعد طُلب منه التعليق؛ لم ينتجها نموذج، وفيها أخطاء مزروعة)

بلغ إجمالي المصروفات الفعلية 2,368,500 ريال، وتجاوز الموازنة بمبلغ 150,500 ريال [Variance!E16]، أي 6.8% [Variance!F16].

الصيانة الميدانية (CC-104): تجاوز بمبلغ 43,100 ريال [Variance!E7]، بنسبة 17.5% [Variance!F7]، بسبب عمل إضافي لإصلاحات طارئة في تكييف مبنى عميل.

الحراسات الأمنية (CC-107): تجاوز بمبلغ 53,600 ريال [Variance!E10]، أي 11.8% [Variance!F10]، بسبب بدء عقد حراسة جديد خلال الشهر.

نظافة المجمعات التجارية (CC-102): تجاوز بمبلغ 34,900 ريال [Variance!E5]، بسبب ارتفاع أسعار مواد النظافة لدى الموردين خلال الربع.

أسطول المركبات (CC-110): وفر بمبلغ 28,300 ريال [Variance!D13]، بنسبة 24.0% [Variance!F13]، لتأجيل استلام مركبتين.

نظافة المباني الحكومية (CC-101): تجاوز بمبلغ 24,800 ريال [Variance!E4]، ويحتاج إلى متابعة.

بقية المراكز ضمن الحدود المقبولة.
""",
"commentary_template.txt": """
تعليق الانحرافات · أكتوبر 2026 · شركة ظِلال لإدارة المرافق
أعدّه: ........  التاريخ: ........  أُعدّت المسودة بمساعد: نعم / لا

قاعدة الكتابة: كل رقم يتبعه عنوان خليته بين قوسين مربعين، مثل: 41,300 ريال [Variance!E7].
لا رقم دون خلية. النسبة تُكتب بخانة عشرية واحدة كما تعرضها الورقة.
قاعدة التعليق: يُعلَّق على المركز حين يبلغ الانحراف 20,000 ريال و10% من موازنته معًا.

الإجمالي: ........

لكل مركز يستوجب التعليق:
  المركز: ........
  الانحراف: ........ ريال [Variance!E..]، بنسبة ........% [Variance!F..]
  السبب: ........
  دليل السبب: (رقم المستند في cc_notes.txt) أو «غير موثق: يُسأل صاحب المركز»
""",
"sampling_plan.txt": """
خطة المعاينة · فحص فواتير الموردين من يناير إلى أكتوبر 2026 · شركة ظِلال (بيانات اصطناعية)
أعدّها مرزوق الغبيني، مدير المراجعة الداخلية، في 1 نوفمبر 2026.

المجتمع: كل أسطر الملف invoices_fy2026.csv. قبل أي سحب يُسجَّل عدد الفواتير ومجموع مبالغها،
ويُطابَقان مع رصيد حساب المشتريات في دفتر الأستاذ.

1. البنود الرئيسة: كل فاتورة مبلغها 100,000 ريال أو أكثر تُفحص كلها، ولا تدخل السحب.
2. الباقي يُرتَّب تصاعديًا برقم الفاتورة invoice_id ويُرقَّم من 1.
3. حجم العينة من الباقي: 60 فاتورة.
4. الطريقة: اختيار منتظم ببداية عشوائية. الفترة = عدد الباقي ÷ 60 مع إهمال الكسر.
   البداية = الجزء الصحيح من (العدد العشوائي الأول × الفترة) + 1، والعدد العشوائي الأول هو أول
   قيمة يعطيها random.Random(البذرة).random() في بايثون.
5. البذرة العشوائية: 20261031. تُسجَّل مع البداية والفترة في ملف المعاينة.
6. الفواتير المختارة: مواضع البداية، ثم البداية + الفترة، وهكذا حتى 60 فاتورة.

الاختبارات على كل فاتورة مفحوصة (البنود الرئيسة والعينة):
  أ. هل لها أمر شراء؟
  ب. هل لها فاتورة أخرى في المجتمع بالمورد نفسه ورقم فاتورة المورد نفسه والمبلغ نفسه؟
  ج. هل تاريخها بعد آخر يوم في فترة ترحيلها؟
  د. هل معها فاتورة أخرى للمورد نفسه في اليوم نفسه، كل منهما دون حد الاعتماد 50,000 ريال
     ومجموعهما يتجاوزه؟

ما يظهر في هذه الاختبارات «بند للنظر». الحكم بأنه استثناء، وسببه، وأثره، للمدقق لا للأداة.
""",
"ai_sample_answer.txt": """
رد المساعد على: «اختر لي 60 فاتورة عشوائية من الملف المرفق لعينة التدقيق»
(رد مكتوب باليد يمثّل مساعد محادثة لا يشغّل رموزًا؛ لم ينتجه نموذج)

بالتأكيد. هذه عينة عشوائية من 60 فاتورة موزعة على الفترة:

{IDS}

اخترتها عشوائيًا بحيث تمثّل الموردين والأشهر تمثيلًا متوازنًا.

حين أُعيد الطلب نفسه في محادثة جديدة بدأت القائمة هكذا:

{SECOND}
""",
"sampling_file_template.txt": """
ملف المعاينة · فواتير الموردين يناير إلى أكتوبر 2026
أعدّه: ........  التاريخ: ........  راجعه: ........

المجتمع: عدد الفواتير ........  مجموع المبالغ ........  (طابقته مع: ........)
البنود الرئيسة (100,000 ريال فأكثر): العدد ........  المجموع ........
الباقي: العدد ........  المجموع ........
فحص المجاميع: الرئيسة + الباقي = المجتمع؟ ........

الطريقة: اختيار منتظم ببداية عشوائية من الباقي مرتبًا برقم الفاتورة
البذرة العشوائية: ........  الفترة: ........  البداية: ........  حجم العينة: ........
الأداة التي نفّذت السحب: ........  (الدفتر المعدّ / رموز ولّدها المساعد وقرأتُها)
مجموع مبالغ العينة: ........

بنود للنظر في الفواتير المفحوصة:
  رقم الفاتورة | الاختبار | ما وجدته في المستندات | حكمي: استثناء أم لا | السبب
  ........

ما أُعطي للمساعد: ........  وما لم يُعطَ: ........
""",
"approved_tools.txt": """
سجل الأدوات المعتمدة للإدارة المالية · شركة ظِلال لإدارة المرافق (جهة افتراضية)
اعتمدته ثريا الحمداني، المراقبة المالية. الشركة تصنّف بياناتها على المستويات الأربعة لسياسة تصنيف
البيانات الوطنية: عام، مقيد، سري، سري للغاية. هذا سجل شركة خاصة افتراضية لغرض التدريب.
تنبيه: في الجهات الحكومية تنص مبادئ الذكاء الاصطناعي التوليدي للجهات الحكومية على ألا يُدخل العاملون
في أدوات الذكاء الاصطناعي التوليدي بيانات مصنفة «مقيد» فأعلى، وأن يقتصر استخدامها على بيانات «عام».
البند 2 أدناه لا يصح في جهة حكومية.

1. مساعدات الذكاء الاصطناعي العامة المجانية (أي مساعد خارج حسابات الشركة):
   بيانات «عام» فقط. لا ملف من ملفات الإقفال يدخلها.

2. «رقيم»، المساعد المعتمد الذي يشغّل الرموز البرمجية داخل بيئة الشركة:
   بيانات «عام» و«مقيد»، بشرط ألا يكون في الملف بيانات شخصية.
   ملف فيه بيانات شخصية لا يدخله إلا بعد حذف الأسماء والهويات والحسابات البنكية أو تجميعه.

3. الأدوات المحلية على جهاز الشركة (جدول البيانات، والدفتر المعدّ مسبقًا):
   كل المستويات التي يحق للموظف الاطلاع عليها.

قاعدة الأثر: كل استخدام للمساعد في رقم يدخل الإقفال يُسجَّل في سجل الاستخدام: التاريخ، والمهمة،
والملفات التي أُعطيت، والمجموع الرقابي الذي أثبت الناتج.
""",
"redesign/redesign_card_template.txt": """
بطاقة إعادة تصميم مهمة متكررة
الاسم: ........  المهمة: ........  تتكرر: أسبوعيًا / شهريًا

1. البيانات والأداة
   الملفات: ........  تصنيفها: ........  فيها بيانات شخصية؟ ........
   الأداة المسموح بها حسب سجل الأدوات: ........

2. الخطوات بعد إعادة التصميم
   الخطوة | من ينفّذها: رموز أو صيغة / المساعد يكتب نصًا / أنا | كيف أعرف أنها صحيحة
   ........

3. المجاميع الرقابية
   قبل التنفيذ: ........  بعد التنفيذ: ........  ما الذي يجب أن يتساوى: ........

4. ما يبقى لحكمي أنا ولا يُفوَّض
   ........

5. القياس
   خط الأساس: متوسط الدقائق ........  متوسط الأخطاء ........  (من كم تنفيذ؟ ........)
   التنفيذ 1 بعد إعادة التصميم: الدقائق ........  الأخطاء ........  المجموع الرقابي يتفق؟ ........
   التنفيذ 2 بعد إعادة التصميم: الدقائق ........  الأخطاء ........  المجموع الرقابي يتفق؟ ........
   ما الذي لا تقوله هذه الأرقام: ........

6. سجل الاستخدام: أين يُحفظ سجل التشغيل وسجل التغييرات؟ ........
""",
"redesign/redesign_card_example.txt": """
بطاقة إعادة تصميم مهمة متكررة · مثال محلول من شركة ظِلال (أرقام التنفيذ بعد إعادة التصميم مثال
وضعه كاتب المقرر، وليست قياسًا)
الاسم: يسرى البواردي  المهمة: مطابقة كشف مورد مع حسابه في الذمم الدائنة  تتكرر: شهريًا

1. البيانات والأداة
   الملفات: supplier_statement.csv وap_ledger_supplier.csv. تصنيفها: مقيد. لا بيانات شخصية.
   الأداة: «رقيم» مسموح. المساعدات العامة غير مسموحة.

2. الخطوات بعد إعادة التصميم
   قراءة الملفين وعدّ الأسطر وجمع المبالغ | رموز | العدد والمجموع يساويان ما في رأس كل ملف
   المطابقة برقم المستند ثم المبلغ | رموز قرأتُ مفتاح الربط فيها | مطابق + غير مطابق = عدد الأسطر
   تصنيف الفروق | أنا | كل فرق له مستند
   مسودة رسالة إلى المورد بالفروق | المساعد يكتب نصًا | كل رقم في الرسالة له سطر في جدول الفروق
   الاعتماد | أنا |

3. المجاميع الرقابية
   قبل: عدد أسطر كل ملف ومجموعه. بعد: رصيد الكشف − رصيد الدفتر = مجموع الفروق المصنفة.

4. ما يبقى لحكمي: هل السداد المكرر خطأ ترحيل أم سداد فعلي مرتين؟ من يتصل بالمورد؟

5. القياس
   خط الأساس: متوسط 46 دقيقة، ومتوسط خطأين، من ثلاثة تنفيذات.
   التنفيذ 1 بعد إعادة التصميم: يُملأ في المختبر 2.4.
   التنفيذ 2: يُملأ قبل جلسة المراجعة، على مهمتك أنت.
   ما لا تقوله الأرقام: ثلاثة تنفيذات وشخص واحد. الفرق مؤشر لا برهان.

6. سجل الاستخدام: سجل تشغيل الدفتر run_log.csv، وملاحظة في ملف الإقفال.
""",
"recon_statement_template.txt": """
قائمة مطابقة حساب البنك · 31 أكتوبر 2026 · شركة ظِلال لإدارة المرافق
أعدّها: ........  راجعها: ........

المجاميع الرقابية
  كشف البنك: عدد الأسطر ........  المجموع ........
  دفتر الأستاذ: عدد الأسطر ........  المجموع ........
  أزواج متطابقة: ........  غير متطابق في البنك: ........  غير متطابق في الدفتر: ........
  الفحص: متطابق + غير متطابق = عدد أسطر كل ملف؟ ........

جهة البنك
  الرصيد الختامي حسب كشف البنك                         ........
  يضاف: إيداعات بالطريق (عددها ....)                   ........
  يطرح: مدفوعات لم تُصرف بعد (عددها ....)              ........
  الرصيد المعدَّل حسب البنك                            ........

جهة الدفتر
  الرصيد الختامي حسب دفتر الأستاذ                      ........
  يُعكس: قيود مكررة (عددها ....)                       ........
  يضاف أو يطرح: بنود في البنك لم تُقيَّد (عددها ....)   ........
  تصحيح: فرق مبلغ في القيد ........                    ........
  الرصيد المعدَّل حسب الدفتر                           ........

الرصيدان المعدَّلان متساويان؟ ........
قيود التسوية المطلوبة ومن يعتمدها: ........
""",
}

_SETUP = '''
# الإعداد: يجد الملفات بجوار الدفتر أو في المجلد الأعلى. في خدمة دفاتر مستضافة: ارفع الملفات بجوار الدفتر.
import csv, datetime, hashlib
from pathlib import Path
import pandas as pd

def find(name):
    for p in (Path("."), Path(".."), Path("files")):
        if (p / name).exists():
            return p / name
    raise FileNotFoundError(name + " : ضع الملف بجوار الدفتر")

def log_run(notebook, inputs, totals):
    """يضيف سطرًا إلى سجل التشغيل: متى، وعلى أي ملفات (بصمتها)، وبأي مجاميع رقابية."""
    stamp = datetime.datetime.now().isoformat(timespec="seconds")
    marks = ";".join(p.name + ":" + hashlib.sha256(p.read_bytes()).hexdigest()[:12] for p in inputs)
    new = not Path("run_log.csv").exists()
    with open("run_log.csv", "a", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["run_at", "notebook", "inputs_sha256", "control_totals"])
        w.writerow([stamp, notebook, marks, totals])
    print("سُجّل التشغيل في run_log.csv")
'''

NOTEBOOKS = {
"reconcile.ipynb": [
("markdown", """
# مطابقة البنك مع دفتر الأستاذ · أكتوبر 2026

دفتر معدّ مسبقًا لشركة ظِلال (بيانات اصطناعية). شغّل الخلايا بالترتيب: لا تحتاج إلى كتابة أي رموز.
الدفتر **يحسب** ويثبت حسابه بمجاميع رقابية، و**يقترح** تصنيفًا للبنود غير المتطابقة. القرار في كل بند لك.
"""),
("code", _SETUP),
("markdown", "## 1 · المجاميع الرقابية قبل أي معالجة"),
("code", '''
OPENING = 2350000.00
bank_path, ledger_path = find("bank_statement_oct.csv"), find("ledger_cash_oct.csv")
bank = pd.read_csv(bank_path, dtype={"reference": str})
ledger = pd.read_csv(ledger_path, dtype={"reference": str})
for df in (bank, ledger):
    df["h"] = (df["amount"] * 100).round().astype("int64")      # المبلغ بالهللات: لا كسور عشرية في المقارنة
    df["key"] = df["reference"].str.strip().str.upper()         # مفتاح الربط: المرجع بعد التنظيف
control_in = {"bank_lines": len(bank), "bank_sum": bank["h"].sum() / 100,
              "ledger_lines": len(ledger), "ledger_sum": ledger["h"].sum() / 100}
print(control_in)
'''),
("markdown", "## 2 · المطابقة بالمرجع ثم المبلغ\n\nكل سطر يُستخدم مرة واحدة: السطر الثاني بالمرجع والمبلغ نفسيهما لا يجد شريكًا ويبقى ظاهرًا."),
("code", '''
for df in (bank, ledger):
    df["n"] = df.groupby(["key", "h"]).cumcount()
m = bank.merge(ledger, on=["key", "h", "n"], how="outer", suffixes=("_bank", "_ledger"), indicator=True)
matched = m[m["_merge"] == "both"]
bank_only = m[m["_merge"] == "left_only"]
ledger_only = m[m["_merge"] == "right_only"]
control_out = {"matched_pairs": len(matched), "matched_sum": matched["h"].sum() / 100,
               "bank_unmatched": len(bank_only), "ledger_unmatched": len(ledger_only)}
print(control_out)
# الفحص الرقابي: لا سطر ضاع ولا سطر استُخدم مرتين
assert len(matched) + len(bank_only) == len(bank), "أسطر البنك لا تتطابق عددًا"
assert len(matched) + len(ledger_only) == len(ledger), "أسطر الدفتر لا تتطابق عددًا"
assert matched["h"].sum() + bank_only["h"].sum() == bank["h"].sum(), "مجموع البنك لا يتطابق"
assert matched["h"].sum() + ledger_only["h"].sum() == ledger["h"].sum(), "مجموع الدفتر لا يتطابق"
print("المجاميع الرقابية متفقة: متطابق + غير متطابق = كل ملف، عددًا ومبلغًا")
'''),
("markdown", "## 3 · البنود غير المتطابقة وتصنيف مقترح\n\nالتصنيف اقتراح من قاعدة مكتوبة أدناه. اقرأ القاعدة، ثم احكم على كل بند من مستنده."),
("code", '''
bank_keys, ledger_keys = set(bank["key"]), set(ledger["key"])
pairs = set(zip(matched["key"], matched["h"]))

def suggest_ledger(r):
    if r["key"] not in bank_keys:
        return "مدفوع لم يُصرف بعد" if r["h"] < 0 else "إيداع بالطريق"
    return "قيد مكرر" if (r["key"], r["h"]) in pairs else "فرق مبلغ"

def suggest_bank(r):
    return "فرق مبلغ" if r["key"] in ledger_keys else "في البنك ولم يُقيَّد"

lo = ledger_only.assign(side="ledger", id=ledger_only["entry_no"], date=ledger_only["date_ledger"],
                        description=ledger_only["description_ledger"], suggested=ledger_only.apply(suggest_ledger, axis=1))
bo = bank_only.assign(side="bank", id=bank_only["line_no"], date=bank_only["date_bank"],
                      description=bank_only["description_bank"], suggested=bank_only.apply(suggest_bank, axis=1))
unmatched = pd.concat([bo, lo])[["side", "id", "date", "key", "description", "h", "suggested"]]
unmatched["amount"] = unmatched["h"] / 100
print(unmatched.groupby(["side", "suggested"])["amount"].agg(["count", "sum"]).round(2))
unmatched.drop(columns="h").to_csv("unmatched_suggested.csv", index=False, encoding="utf-8-sig")
'''),
("markdown", "## 4 · قائمة المطابقة\n\nالرصيدان المعدَّلان يجب أن يتساويا. إن لم يتساويا فهناك بند لم يُصنَّف صحيحًا."),
("code", '''
def total(side, label):
    x = unmatched[(unmatched["side"] == side) & (unmatched["suggested"] == label)]
    return len(x), x["h"].sum() / 100

bank_closing = round(OPENING + control_in["bank_sum"], 2)
ledger_closing = round(OPENING + control_in["ledger_sum"], 2)
n_dep, dep = total("ledger", "إيداع بالطريق")
n_out, out = total("ledger", "مدفوع لم يُصرف بعد")
n_dup, dup = total("ledger", "قيد مكرر")
n_bo, bo_sum = total("bank", "في البنك ولم يُقيَّد")
_, err_bank = total("bank", "فرق مبلغ")
_, err_ledger = total("ledger", "فرق مبلغ")
adjusted_bank = round(bank_closing + dep + out, 2)
adjusted_ledger = round(ledger_closing - dup + bo_sum + (err_bank - err_ledger), 2)
statement = {"bank_closing": bank_closing, "deposits_in_transit": (n_dep, dep), "outstanding_payments": (n_out, out),
             "adjusted_bank": adjusted_bank, "ledger_closing": ledger_closing, "duplicates": (n_dup, dup),
             "bank_only": (n_bo, bo_sum), "amount_correction": round(err_bank - err_ledger, 2), "adjusted_ledger": adjusted_ledger}
for k, v in statement.items():
    print(f"{k:22} {v}")
print("الرصيدان المعدَّلان متساويان:", adjusted_bank == adjusted_ledger)
'''),
("code", '''
log_run("reconcile", [bank_path, ledger_path],
        f"bank {control_in['bank_lines']}/{control_in['bank_sum']:.2f}; ledger {control_in['ledger_lines']}/{control_in['ledger_sum']:.2f}; "
        f"matched {control_out['matched_pairs']}; adjusted {adjusted_bank:.2f}/{adjusted_ledger:.2f}")
'''),
],
"commentary_check.ipynb": [
("markdown", """
# فحص تعليق الانحرافات مقابل الخلايا · أكتوبر 2026

يقرأ نص التعليق، ويستخرج كل رقم يتبعه عنوان خلية مثل `41,300 ريال [Variance!E7]`، ويقارنه بقيمة الخلية
في `variance_oct.xlsx`. ثم يسرد الأرقام التي لا خلية لها. لا يحكم على الأسباب: هذا لك.
"""),
("code", _SETUP),
("code", '''
import re
from openpyxl import load_workbook
COMMENTARY = "ai_draft_commentary.txt"     # غيّره إلى ملف تعليقك، مثل my_commentary.txt
text_path, book_path = find(COMMENTARY), find("variance_oct.xlsx")
text = text_path.read_text(encoding="utf-8")
sheet = load_workbook(book_path, data_only=True)["Variance"]
TAG = re.compile(r"(\\d[\\d,]*(?:\\.\\d+)?)\\s*(%?)\\s*(?:ريال)?\\s*\\[Variance!([A-F]\\d+)\\]")
rows = []
for num, pct, cell in TAG.findall(text):
    stated = float(num.replace(",", ""))
    value = sheet[cell].value
    if value is None:
        raise SystemExit("الخلية " + cell + " بلا قيمة محفوظة: افتح الملف في جدول البيانات واحفظه ثم أعد التشغيل")
    shown = round(abs(value) * 100, 1) if pct else round(abs(value))
    rows.append({"cell": cell, "stated": stated, "in_cell": shown, "match": stated == shown})
tags = pd.DataFrame(rows)
print(tags.to_string(index=False))
print("أرقام لها خلية:", len(tags), "· مطابقة:", int(tags["match"].sum()), "· غير مطابقة:", int((~tags["match"]).sum()))
'''),
("code", '''
# أرقام بفواصل آلاف لا يتبعها عنوان خلية
untagged = [n for n in re.findall(r"\\d{1,3}(?:,\\d{3})+(?![\\d,])(?!\\s*(?:ريال)?\\s*\\[Variance!)", text)]
print("أرقام بلا خلية:", untagged)
# المراكز التي تستوجب التعليق حسب القاعدة: 20,000 ريال و10% معًا
material = [sheet[f"A{r}"].value for r in range(4, 16)
            if abs(sheet[f"E{r}"].value) >= 20000 and abs(sheet[f"F{r}"].value) >= 0.10]
missing = [c for c in material if c not in text]
extra = [sheet[f"A{r}"].value for r in range(4, 16) if sheet[f"A{r}"].value in text and sheet[f"A{r}"].value not in material]
print("تستوجب التعليق:", material)
print("غائبة عن النص:", missing, "· معلَّق عليها وهي دون القاعدة:", extra)
log_run("commentary_check", [text_path, book_path],
        f"tags {len(tags)}; match {int(tags['match'].sum())}; untagged {len(untagged)}; missing {len(missing)}")
'''),
],
"audit_sample.ipynb": [
("markdown", """
# سحب عينة تدقيق قابلة لإعادة الإنتاج · فواتير الموردين 2026

ينفّذ خطة المعاينة في `sampling_plan.txt` كما كُتبت: مجاميع المجتمع، ثم البنود الرئيسة، ثم اختيار منتظم
ببداية عشوائية من بذرة مسجَّلة. من يعيد التشغيل بالبذرة نفسها على الملف نفسه يحصل على الفواتير نفسها.
"""),
("code", _SETUP),
("code", '''
import random
SEED, SIZE, KEY_ITEM, LIMIT = 20261031, 60, 100000, 50000
inv_path = find("invoices_fy2026.csv")
inv = pd.read_csv(inv_path, dtype=str, keep_default_na=False)
inv["h"] = (inv["amount"].astype(float) * 100).round().astype("int64")
population = {"count": len(inv), "sum": inv["h"].sum() / 100}
key_items = inv[inv["h"] >= KEY_ITEM * 100]
rest = inv[inv["h"] < KEY_ITEM * 100].sort_values("invoice_id").reset_index(drop=True)
assert len(key_items) + len(rest) == len(inv) and key_items["h"].sum() + rest["h"].sum() == inv["h"].sum()
print("المجتمع:", population)
print("البنود الرئيسة:", len(key_items), key_items["h"].sum() / 100, "· الباقي:", len(rest), rest["h"].sum() / 100)
'''),
("code", '''
interval = len(rest) // SIZE
start = int(random.Random(SEED).random() * interval) + 1          # أول عدد عشوائي من البذرة يحدد البداية
positions = [start + interval * k for k in range(SIZE)]           # مواضع تبدأ من 1
sample = rest.iloc[[p - 1 for p in positions]]
print("البذرة:", SEED, "· الفترة:", interval, "· البداية:", start, "· حجم العينة:", len(sample))
print("مجموع مبالغ العينة:", sample["h"].sum() / 100)
print(sample["invoice_id"].head(5).tolist(), "...", sample["invoice_id"].tail(2).tolist())
'''),
("markdown", "## الاختبارات الأربعة على الفواتير المفحوصة\n\nما يظهر هنا «بند للنظر». هل هو استثناء؟ هذا حكم المدقق بعد قراءة المستند."),
("code", '''
tested = pd.concat([key_items.assign(source="بند رئيس"), sample.assign(source="العينة")])
twin = inv.duplicated(["supplier_id", "supplier_invoice_no", "h"], keep=False)
period_end = pd.to_datetime(inv["posting_period"] + "-01") + pd.offsets.MonthEnd(0)
late = pd.to_datetime(inv["invoice_date"]) > period_end
under = inv[inv["h"] < LIMIT * 100]
g = under.groupby(["supplier_id", "invoice_date"])["h"].agg(["count", "sum"])
split_keys = set(g[(g["count"] > 1) & (g["sum"] >= LIMIT * 100)].index)
split = inv.apply(lambda r: r["h"] < LIMIT * 100 and (r["supplier_id"], r["invoice_date"]) in split_keys, axis=1)
flags = pd.DataFrame({"invoice_id": inv["invoice_id"], "بلا أمر شراء": inv["po_number"] == "", "لها فاتورة مطابقة": twin,
                      "تاريخها بعد فترة الترحيل": late, "تجزئة دون حد الاعتماد": split})
look = tested[["invoice_id", "source", "supplier_id", "amount"]].merge(flags, on="invoice_id")
look = look[look.iloc[:, 4:].any(axis=1)]
print(look.to_string(index=False))
'''),
("code", '''
out = tested[["invoice_id", "source", "supplier_id", "supplier_invoice_no", "invoice_date", "amount", "po_number"]].merge(flags, on="invoice_id")
out["حكم المدقق"] = ""
out.to_csv("sampling_file.csv", index=False, encoding="utf-8-sig")
with open("sampling_file.csv", "a", encoding="utf-8-sig", newline="") as f:
    f.write(f"# method=systematic with random start; seed={SEED}; interval={interval}; start={start}; size={SIZE}; "
            f"population={population['count']}/{population['sum']:.2f}; key_items={len(key_items)}/{key_items['h'].sum() / 100:.2f}\\n")
log_run("audit_sample", [inv_path],
        f"population {population['count']}/{population['sum']:.2f}; key {len(key_items)}; seed {SEED}; start {start}; interval {interval}; "
        f"sample {len(sample)}/{sample['h'].sum() / 100:.2f}; to_look_at {len(look)}")
'''),
],
}
