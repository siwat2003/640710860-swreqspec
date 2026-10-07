# agent-pack สำหรับ repo <ทีม>-swreqspec

ชุดไฟล์คำสั่งที่ทำให้ Copilot, Claude Code และ Cursor มีคำสั่งเหมือนกันทั้ง 3 เครื่องมือ
ไม่ต้องติดตั้งโปรแกรมเพิ่ม แค่วางไฟล์ลง repo แล้ว commit

## คำสั่งทั้งหมด (เรียงตามลำดับที่ใช้)

| คำสั่ง | ได้อะไร | ใช้ครั้งแรกเมื่อ |
|---|---|---|
| `/clarify` | AI ถามคำถามจาก spec.md แล้วแก้เป็น spec v2 | สัปดาห์ Clarify and Plan |
| `/plan` | plan.md แผนทางเทคนิค | สัปดาห์ Clarify and Plan |
| `/tasks` | tasks.md แบ่งเป็นเฟสแนวตั้ง มีจุดตรวจท้ายเฟส | สัปดาห์ tasks.md (รุ่นเฟสเริ่มใช้กับ use case ที่ 2) |
| `/implement T-xx` | โค้ดและ test ของ task 1 ตัว | สัปดาห์ tasks.md |
| `/implement-all เฟส N` | ทำ task ในเฟสต่อเนื่อง commit ทีละ task แล้วหยุดที่จุดตรวจ | สัปดาห์ Verifying (ใช้หลังตรวจเป็นแล้ว) |
| `/testcases AC-xx` | ร่าง test cases จาก AC ลง test-cases.md แล้วเขียนโค้ด test จากแถวที่ทีมตรวจแล้ว | สัปดาห์ Verifying |
| `/verify` | ตารางตามรอย spec โค้ด test (rtm.md) และข้อค้นพบ ไม่แก้โค้ด | สัปดาห์ Verifying |

## ไฟล์ในชุด

| ไฟล์ | ใครอ่าน |
|---|---|
| `AGENTS.md` | Copilot, Cursor อ่านเองทุกครั้ง (กติกา 7 ข้อ) |
| `CLAUDE.md` | Claude Code (ชี้ไปที่ AGENTS.md) |
| `.github/prompts/*.prompt.md` | Copilot |
| `.claude/commands/*.md` | Claude Code |
| `.cursor/commands/*.md` | Cursor |
| `docs/implement-all-guide.md` | คู่มือเฟสแนวตั้งและ /implement-all |

เนื้อหาคำสั่งทั้ง 3 เครื่องมือเหมือนกัน ต่างกันแค่โฟลเดอร์ที่วาง

## อัปเดตคำสั่งใน repo ทีม (ไม่แตะ specs และโค้ดของทีม)

เปิด terminal ที่โฟลเดอร์บนสุดของ repo แล้วรัน

```bash
curl -sL https://github.com/ppsajja/swreqspec-template/archive/refs/heads/main.tar.gz | tar xz --strip-components=1 --wildcards '*/.github/prompts/*' '*/.claude/commands/*' '*/.cursor/commands/*' '*/docs/implement-all-guide.md' '*/docs/agent-pack-README.md'
git add -A && git commit -m "update agent-pack" && git push
```

คำสั่งนี้เขียนทับเฉพาะไฟล์คำสั่งของ AI และคู่มือ 2 ไฟล์ ไม่แตะ AGENTS.md specs backend frontend และ README ของทีม
ถ้าต้องการ AGENTS.md รุ่นล่าสุดด้วย ให้เปิดไฟล์ใน template แล้วคัดลอกหัวข้อ "ไฟล์สำคัญ" ไปวางเอง (ทีมอาจแก้ AGENTS.md ของตัวเองไว้แล้ว)

## ถ้าเครื่องมือใช้ไม่ได้

เปิดไฟล์คำสั่งใน `.github/prompts/` คัดลอกเนื้อหาทั้งหมด วางในแชต AI ตัวไหนก็ได้ ตามด้วย path ของไฟล์ที่ต้องการ
