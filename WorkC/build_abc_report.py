"""Rebuild the concise four-page report, preserving the original Part A page."""
from pathlib import Path
import csv
from statistics import mean, stdev
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'WorkC' / 'outputs'
TMP = ROOT / 'tmp' / 'pdfs'
OUT = ROOT / 'output' / 'pdf'
SOURCE = Path('C:/Users/byeon/Downloads/Individual Musical-Feature Profiles and Initial Liking (2).pdf')

def rows(name):
    with (DATA / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))

rates = rows('error_rates.csv')
effects = rows('effect_summary.csv')
single = rows('single_results.csv')
examples = [('Effect present', rows('single_effect.csv')), ('No effect', rows('single_null.csv'))]
# The prose below describes the original report settings; stop on changed results.
assert all(abs(float(r['estimate']) - expected) < 1e-12
           for r, expected in zip(rates, [0.0466, 0.05, 0.95]))
assert all(int(r['studies']) == 5000 for r in rates)
OUT.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='ArialBold', italic='Arial', boldItalic='ArialBold')
styles = {
    'title': ParagraphStyle('title', fontName='ArialBold', fontSize=15, leading=19, spaceAfter=12),
    'h': ParagraphStyle('h', fontName='ArialBold', fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=5, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Arial', fontSize=10.5, leading=14.1, spaceAfter=7),
    'caption': ParagraphStyle('caption', fontName='Arial', fontSize=8.8, leading=11.4, spaceBefore=4, spaceAfter=8),
    'cell': ParagraphStyle('cell', fontName='Arial', fontSize=9, leading=11.3),
    'cellhead': ParagraphStyle('cellhead', fontName='ArialBold', fontSize=9, leading=11.3),
}
story = []

def p(text, kind='body'):
    story.append(Paragraph(text, styles[kind]))

def table(headers, content, widths):
    cells = [[Paragraph(escape(str(v)), styles['cellhead']) for v in headers]]
    cells += [[Paragraph(escape(str(v)), styles['cell']) for v in row] for row in content]
    item = Table(cells, colWidths=widths, repeatRows=1, hAlign='LEFT')
    item.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#edf0f2')),
        ('LINEBELOW', (0, 0), (-1, 0), .6, colors.HexColor('#88959e')),
        ('LINEBELOW', (0, -1), (-1, -1), .4, colors.HexColor('#b8c0c6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.extend([item, Spacer(1, 5)])

def fig(name, caption):
    item = Image(str(DATA / name))
    item.drawHeight *= 452 / item.drawWidth
    item.drawWidth = 452
    story.append(item)
    p(caption, 'caption')

def f(value):
    return f'{float(value):.2f}'

def group_summary(data, condition):
    scores = [float(row['liking']) for row in data if row['condition'] == condition]
    assert len(scores) == 60
    return f'{mean(scores):.2f} ({stdev(scores):.2f})'

p('Part B  Synthetic data', 'title')
p('How the data were generated', 'h')
p("To examine the study proposed in Part A, we generated data for 120 participants and randomly assigned 60 to each condition. Each row represented one participant's mean initial-liking score, measured from 0 to 100. We generated this final mean directly, rather than simulating the preference task and the four separate melody ratings. This keeps the analysis at the participant level, as planned in Part A.")
p('The four binary profile features were sampled independently, with equal probabilities for their two levels. They represented participant profiles but did not independently influence the simulated score. Before applying the score limits, mismatched scores followed a normal distribution with mean 55 and standard deviation 15. Matched scores had the same standard deviation and mean 55 + delta. The standard deviation describes variation between participant means.')
p('We used delta = 10 points for the dataset with a true effect and delta = 0 for the dataset without an effect. These are hypothetical parameters. Scores below 0 were set to 0, and scores above 100 were set to 100; scores were not rounded. Seed 42 was used for both examples, keeping profiles, assignments and noise identical so that only the effect parameter changed.')
p('What the two datasets look like', 'h')
fig('report_datasets.png', '<b>Figure 1.</b> Distributions of participant mean liking scores. Triangles show means, horizontal lines inside boxes show medians, and boxes show the middle 50% of scores.')
table(['Scenario', 'Mismatched mean (SD)', 'Matched mean (SD)'],
      [[label, group_summary(data, 'mismatched'), group_summary(data, 'matched')] for label, data in examples], [108, 172, 172])
p('<b>Table 1.</b> Descriptive statistics, with 60 participants in each group.', 'caption')
p('The values fall within the intended rating scale, and neither example contains a score exactly at 0 or 100. In the effect-present dataset, the matched group is shifted upward, as expected from the research hypothesis, although the groups still overlap. In the no-effect dataset, the distributions largely overlap; a small difference remains because of random sampling.')

story.append(PageBreak())
p('Part C  Assumptions and analysis', 'title')
p('An independent-samples t test addresses our question because we compare the mean liking scores of two separate groups. We used the two-sided Welch version at alpha = .05 because it does not require equal variances. Although Part A proposed Welch when variances differed, we fixed this method for every analysis rather than switching tests after inspecting the data. Each participant contributed one independent outcome.')
fig('report_qq.png', '<b>Figure 2.</b> Normal Q-Q plots for each group. Most points follow the reference line, with some tail departures in the mismatched group. The shapes repeat because the examples use identical noise and no scores were clipped.')
p('The Q-Q plots suggest no severe departure from normality, and the boxplots show no isolated outliers. Group standard deviations were 13.93 and 16.34 points. Welch allows this difference in spread. No transformation or removal of observations was applied. These checks do not prove the assumptions; selecting a method on the same data to obtain significance could increase false positives, so the analysis rule was fixed.')
p('Results for the two datasets', 'h')
table(['Scenario', 'Mean difference', '95% CI', 'p-value'],
      [[r['scenario'], f(r['difference']), f"[{f(r['ci_low'])}, {f(r['ci_high'])}]", f"{float(r['p_value']):.3g}"] for r in single], [106, 100, 151, 95])
p('<b>Table 2.</b> Mean difference = matched minus mismatched, in points.', 'caption')
p('The effect-present dataset showed a positive, statistically significant difference; its confidence interval excluded zero. The no-effect dataset did not reject the null, but this does not prove the absence of an effect. The estimates differ from the input values of 10 and 0 because of random sampling. Their variation depends on sample size and score variability. Limiting scores to 0-100 can also slightly change the population mean difference.')

story.append(PageBreak())
p('Part C  Repeated simulation', 'title')
p('We ran 5,000 studies with an effect and 5,000 without one. Each repetition generated a new dataset with 60 participants per group, applied the same Welch test and saved the results. Master seed 20260929 provided separate random streams for the studies. We recorded the mean difference, p-value, confidence interval and whether p was below .05. The analysis included every study, regardless of significance.')
fig('report_effects.png', '<b>Figure 3.</b> Estimated mean differences from 5,000 studies per scenario. Dashed lines show the input differences of 0 and 10 points, before scores were limited to 0-100.')
table(['Scenario', 'Mean estimated effect', 'SD of estimates', 'Significant studies'],
      [[label, f(r['mean_estimate']), f(r['sd_across_studies']), f"{int(r['significant_studies']):,} / 5,000"] for label, r in zip(['No effect', 'Effect present'], effects)], [101, 128, 103, 120])
p('<b>Table 3.</b> Effects and standard deviations are in points. All studies are included.', 'caption')
p('Error rates and power', 'h')
p('<b>Type I error was 4.66%:</b> 233 of the 5,000 no-effect studies incorrectly rejected the null. This is close to the chosen 5% significance level. <b>Power was 95.00%:</b> 4,750 of the 5,000 effect-present studies detected a difference. <b>Type II error was 5.00%:</b> the remaining 250 studies missed the effect.')
p('Interpretation', 'h')
p('The average estimated difference was -0.01 points without an effect and 9.92 points with an effect. The standard deviations of 2.69 and 2.72 points show how much estimates vary between studies. Thus, even researchers using the same design can obtain different results simply because they sample different participants.')
p('With more participants per group, we would expect less variation in estimated effects, narrower confidence intervals and higher power. Smaller effects or greater score variability would make detection harder. Increasing simulation repetitions instead makes the estimated rates more stable, without changing the precision of each individual study.')
p('For the chosen parameters, the proposed design usually detects the effect while keeping false positives near 5%. These findings depend on the simplified data-generation model. They evaluate the planned analysis and do not provide real-world evidence that matching music to a profile increases liking.')

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Arial', 8.5)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(72, 35, 'Individual Musical-Feature Profiles and Initial Liking')
    canvas.drawRightString(524, 35, str(doc.page + 1))
    canvas.restoreState()

bc = TMP / 'parts_bc.pdf'
doc = SimpleDocTemplate(str(bc), pagesize=(596, 842), rightMargin=72, leftMargin=72,
                        topMargin=55, bottomMargin=53, title='Individual Musical-Feature Profiles and Initial Liking Parts B and C', author='Nahyeon Kang')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
reader_a, reader_bc = PdfReader(SOURCE), PdfReader(bc)
assert len(reader_a.pages) == 1 and len(reader_bc.pages) == 3
writer = PdfWriter()
writer.append(reader_a)
writer.append(reader_bc)
writer.add_metadata({'/Title': 'Individual Musical-Feature Profiles and Initial Liking - Parts A B C', '/Author': 'Nahyeon Kang'})
for index, title in enumerate(['Part A Research proposal', 'Part B Synthetic data', 'Part C Assumptions and analysis', 'Part C Repeated simulation']):
    writer.add_outline_item(title, index)
target = OUT / 'ADAMS_Report_ABC.pdf'
with target.open('wb') as stream:
    writer.write(stream)
final = PdfReader(target)
assert len(final.pages) == 4
assert final.pages[0].get_contents().get_data() == reader_a.pages[0].get_contents().get_data()
assert final.pages[0].extract_text() == reader_a.pages[0].extract_text()
print(f'Created {target}; original Part A preserved.')
