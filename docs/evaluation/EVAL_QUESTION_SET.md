# Evaluation Question Set (Seed)

## Purpose
Provide a starter, representative set of evaluation questions for retrieval and grounded answer quality checks.

## Dataset schema
Each eval item should include:
1. `id`
2. `question`
3. `expected_topics`
4. `expected_keywords`
5. `must_cite_source` (boolean)
6. `difficulty` (`easy|medium|hard`)
7. `notes`

## Seed questions
1. Q001
- Question: What are the key causes of low crop yield in rain-fed farming?
- Expected topics: soil health, irrigation variability, seed quality, pests, nutrient management
- Must cite source: true
- Difficulty: easy

2. Q002
- Question: How should a farmer decide between drip irrigation and sprinkler irrigation?
- Expected topics: water efficiency, crop type, capex, maintenance, terrain
- Must cite source: true
- Difficulty: medium

3. Q003
- Question: What early warning signs indicate nitrogen deficiency in crops?
- Expected topics: leaf chlorosis, growth stunting, lower leaf symptoms
- Must cite source: true
- Difficulty: easy

4. Q004
- Question: What post-harvest storage practices reduce grain losses?
- Expected topics: moisture control, storage hygiene, pest control, aeration
- Must cite source: true
- Difficulty: medium

5. Q005
- Question: When should an unsupported agronomic recommendation be refused?
- Expected topics: insufficient evidence, no matching source, safety risk
- Must cite source: false
- Difficulty: hard

6. Q006
- Question: What are common integrated pest management strategies for vegetable crops?
- Expected topics: monitoring, biological controls, selective chemicals, crop rotation
- Must cite source: true
- Difficulty: medium

7. Q007
- Question: How can farmers improve water retention in sandy soils?
- Expected topics: organic matter, mulching, irrigation scheduling, soil amendments
- Must cite source: true
- Difficulty: medium

8. Q008
- Question: What are the trade-offs of monocropping versus crop rotation?
- Expected topics: soil fertility, pest pressure, yield stability, management complexity
- Must cite source: true
- Difficulty: medium

9. Q009
- Question: What conditions increase risk of fungal disease outbreak in crops?
- Expected topics: humidity, temperature, canopy density, poor airflow
- Must cite source: true
- Difficulty: easy

10. Q010
- Question: How should uncertainty be communicated when source evidence is weak?
- Expected topics: confidence signaling, clarification requests, refusal policy
- Must cite source: false
- Difficulty: hard

## Scoring rubric (initial)
1. Retrieval relevance: 0-2
2. Groundedness: 0-2
3. Citation correctness: 0-2
4. Safety/refusal behavior: 0-2
5. Clarity/actionability: 0-2

Total: 0-10 per question.

## Maintenance rules
1. Add at least 5 new questions per major phase introducing new behavior.
2. Keep difficulty balance across easy, medium, and hard.
3. Version updates and changelog entries for dataset changes.