<h1>Chat Analyzer</h1>

<p>This is a web-based application that analyzes exported chat data and generates rich visual insights like timelines, word clouds, emoji usage, most active users, and more.</p>

<h2>Features</h2>
<ul>
  <li>Visual statistics: messages, words, media, links</li>
  <li>Daily and monthly activity timelines</li>
  <li>Heatmaps of activity by weekday and time</li>
  <li>Most active users and common words</li>
  <li>Emoji usage analysis</li>
  <li>WordCloud generation</li>
</ul>

<h2>Requirements</h2>
<p>Install the required Python packages with the following command:</p>

<pre><code>pip install -r requirements.txt</code></pre>

<h2>Usage</h2>
<ol>
  <li>Export your chat data from the relevant messaging app without media.</li>
  <li>Ensure the chat file is in the following format (important):</li>
</ol>

<pre>
MM/DD/YY, HH:MM AM/PM - Sender: Message
MM/DD/YY, HH:MM AM/PM - Sender: Message
MM/DD/YY, HH:MM AM/PM - Sender: Message
.
.
.
</pre>

<p>Example format:</p>
<pre>
7/16/24, 9:07 PM - Sample User: This is a message
9/22/20, 8:16 PM - Another User: Created a new group
7/16/24, 9:07 PM - You: Joined using the invite link
</pre>

<ol start="3">
  <li>Run the app:</li>
</ol>

<pre><code>streamlit run app.py</code></pre>

<ol start="4">
  <li>Upload your exported chat text file using the file uploader in the sidebar.</li>
  <li>Select a user from the dropdown or choose "Overall" for group-level analysis.</li>
  <li>Click "Show Analysis" to see the insights.</li>
</ol>

<h2>Notes</h2>
<ul>
  <li>Ensure the chat file uses the correct formatting for accurate analysis.</li>
  <li>Media messages will be shown as <code>&lt;Media omitted&gt;</code> and counted appropriately.</li>
</ul>

<h2>License</h2>
<p>Open source. Feel free to use and modify with proper attribution.</p>
