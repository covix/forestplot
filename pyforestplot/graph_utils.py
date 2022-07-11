import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
from typing import Optional, List, Union, Tuple
import warnings
warnings.filterwarnings("ignore")


def draw_ci(
	dataframe: pd.core.frame.DataFrame,
	estimate: str,
	yticklabel: str,
	moerror: str,
	ax: Axes,
	**kwargs
) -> Axes:
	"""
	Draw the confidence intervals using the horizontal bar plot (barh) from the pandas API.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	estimate (str)
		Name of column containing the estimates (e.g. pearson correlation coefficient,
		OR, regression estimates, etc.).
	yticklabel (str)
		Name of column in intermediate dataframe containing the formatted yticklabels.
	moerror (str)
		Name of column containing the margin of error in the confidence intervals.
		Should be available if 'll' and 'hl' are left empty.
	ax (Matplotlib Axes)
		Axes to operate on.
	
	Returns
	-------
		Matplotlib Axes object.
	"""
	lw = kwargs.get("lw", 0.5)

	ax = dataframe.plot(
		y=estimate,
		x=yticklabel,
		kind="barh",
		xerr=moerror,
		color="none",
		error_kw={"lw": lw},
		legend=False,
		ax=ax,
	)

	return ax


def draw_est_markers(
	dataframe: pd.core.frame.DataFrame, estimate: str, yticklabel: str, ax, **kwargs
) -> Axes:
	"""
	Draws the markers of the estimates using the Matplotlib plt.scatter API.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	estimate (str)
		Name of column containing the estimates (e.g. pearson correlation coefficient,
		OR, regression estimates, etc.).
	yticklabel (str)
		Name of column in intermediate dataframe containing the formatted yticklabels.
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------
		Matplotlib Axes object.
	"""
	marker = kwargs.get("marker", "s")
	markersize = kwargs.get("markersize", 20)
	markercolor = kwargs.get("markercolor", "navy")

	ax.scatter(
		y=yticklabel,
		x=estimate,
		data=dataframe,
		marker=marker,
		s=markersize,
		color=markercolor,
	)

	return ax


def draw_ref_xline(ax: Axes, **kwargs):
	"""
	Draw the vertical reference xline at zero. Unless defaults are overridden in kwargs.

	Parameters
	----------
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------
		Matplotlib Axes object.
	"""
	xline = kwargs.get("xline", 0)
	xlinestyle = kwargs.get("xlinestyle", "-")
	xlinecolor = kwargs.get("xlinecolor", "k")
	xlinewidth = kwargs.get("xlinewidth", 0.8)
	ax.axvline(x=xline, linestyle=xlinestyle, color=xlinecolor, linewidth=xlinewidth)
	return ax


def right_flush_yticklabels(
	dataframe: pd.core.frame.DataFrame, yticklabel: str, flush: bool, ax: Axes, **kwargs
) -> float:
	"""
	Flushes the formatted ytickers to the left. Also returns the amount of max padding in the
	window width. Padding to be used for drawing the 2nd yticklabels and ylabels.

	My reference: https://stackoverflow.com/questions/15882249/matplotlib-aligning-y-ticks-to-the-left

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	yticklabel (str)
		Name of column in intermediate dataframe containing the formatted yticklabels.
	flush (bool)
		Left-flush the variable labels.
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------
		Window wdith of figure (float)
	"""
	fontfamily = kwargs.get("fontfamily", "monospace")

	plt.draw()  # this is needed because get_window_extent needs a renderer to work
	fig = plt.gcf()
	if flush:
		ax.set_yticklabels(dataframe[yticklabel], fontfamily=fontfamily, ha="left")
	else:
		ax.set_yticklabels(dataframe[yticklabel], fontfamily=fontfamily, ha="right")

	yax = ax.get_yaxis()
	pad = max(
		T.label.get_window_extent(renderer=fig.canvas.get_renderer()).width
		for T in yax.majorTicks
	)
	if flush:  # Flush yticklabels to left
		yax.set_tick_params(pad=pad)

	return pad


def draw_pval_right(
	dataframe: pd.core.frame.DataFrame,
	pval: str,
	annoteheaders: Union[list, tuple],
	yticklabel: str,
	pad: float,
	ax: Axes,
	**kwargs
) -> Axes:
	"""
	Draws the 2nd ytick labels on the right-hand side of the figure.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	pval (str)
		Name of column containing the p-values.
	annoteheaders (list-like)
		List of table headers to use as column headers for the additional annotations.
	yticklabel (str)
		Name of column in intermediate dataframe containing the formatted yticklabels.
	pad (float)
		Window wdith of figure
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------
		Matplotlib Axes object.		
	"""
	if pval is not None:
		for _, row in dataframe.iterrows():
			yticklabel1 = row[yticklabel]
			yticklabel2 = row['formatted_pval']
			if pd.isna(yticklabel2):
				yticklabel2 = ''

			extrapad = 0.05
			pad = ax.get_xlim()[1] * (1 + extrapad)
			ax.text(
				x=pad,
				y=yticklabel1,
				s=yticklabel2,
				horizontalalignment="left",
				verticalalignment="center",
			)

		# 2nd label title
		pval_title = kwargs.get('pval_title', 'P-value')
		if pval_title is not None:
			if annoteheaders is None:
				ax.text(pad, ax.get_ylim()[1], pval_title, size=10, fontweight="bold")

			if annoteheaders is not None:  # if tableheaders exist
				pval_title_fontweight = kwargs.get("pval_title_fontweight", "bold")
				pval_title_fontsize = kwargs.get("pval_title_fontsize", 10)

				header_index = len(ax.get_yticklabels()) - 1
				ax.text(
					x=pad,
					y=header_index,
					s=pval_title,
					size=pval_title_fontsize,
					fontweight=pval_title_fontweight,
					horizontalalignment="left",
					verticalalignment="center",
				)

	return ax


def draw_ylabel2(dataframe: pd.core.frame.DataFrame, ax: Axes, **kwargs):
	"""
	Draw the second ylabel title on the right-hand side y-axis.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------
		Matplotlib Axes object.
	"""
	grouplab_size = kwargs.get("grouplab_size", 10)
	grouplab_fontweight = kwargs.get("grouplab_fontweight", "bold")

	group_row_ix = len(dataframe) - 1

	for ix, row in dataframe.iterrows():
		yticklabel1 = row["yticklabel"]
		yticklabel2 = row["yticklabel2"]

		extrapad = 0.05
		pad = ax.get_xlim()[1] * (1 + extrapad)
		if ix == group_row_ix:
			ax.text(
				x=pad,
				y=yticklabel1,
				s=yticklabel2,
				fontfamily="monospace",
				horizontalalignment="left",
				verticalalignment="center",
				fontweight=grouplab_fontweight,
				fontsize=grouplab_size,
			)
		else:
			ax.text(
				x=pad,
				y=yticklabel1,
				s=yticklabel2,
				fontfamily="monospace",
				horizontalalignment="left",
				verticalalignment="center",
			)

	return ax


def draw_ylabel1(ylabel: str, pad: float, ax: Axes, **kwargs) -> Axes:
	"""
	Draw ylabel title for the left-hand side y-axis.

	Parameters
	----------
	ylabel (str)
		Title of the left-hand side y-axis.
	pad (float)
		Window wdith of figure
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------	
		Matplotlib Axes object.
	"""
	ax.set_ylabel("")
	if ylabel is not None:

		# Retrieve settings from kwargs
		ylabel1_size = kwargs.get("ylabel1_size", 12)
		ylabel1_fontweight = kwargs.get("ylabel1_fontweight", "bold")
		ylabel_loc = kwargs.get("ylabel_loc", "top")
		ylabel_angle = kwargs.get("ylabel_angle", "horizontal")

		# Draw ylabel
		ax.set_ylabel(
			ylabel,
			loc=ylabel_loc,
			labelpad=-pad,
			rotation=ylabel_angle,
			size=ylabel1_size,
			fontweight=ylabel1_fontweight,
		)

	return ax


def remove_ticks(ax: Axes) -> Axes:
	"""
	Removes the tickers on the top, left, and right borders.

	Parameters
	----------
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------	
		Matplotlib Axes object.
	"""
	ax.tick_params(
		top=False,
		bottom=True,
		left=False,
		right=False,
		labelleft=True,
		labelright=False,
		labelbottom=True,
	)
	return ax


def format_grouplabels(
	dataframe: pd.core.frame.DataFrame, groupvar: str, ax: Axes, **kwargs
) -> Axes:
	"""
	Bold the group variable labels.

	Fontweight options in Matplotlib: [ 'normal' | 'bold' | 'heavy' | 'light' | 'ultrabold' | 'ultralight' ]

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	groupvar (str)
		Name of column containing group of variables.
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------	
		Matplotlib Axes object.	
	"""
	grouplab_size = kwargs.get("grouplab_size", 10)
	grouplab_fontweight = kwargs.get("grouplab_fontweight", "bold")

	if groupvar is not None:
		for ix, ylabel in enumerate(ax.get_yticklabels()):
			for gr in dataframe[groupvar].unique():
				try:
					if gr.lower() == ylabel.get_text().lower().strip():
						ax.get_yticklabels()[ix].set_fontweight(grouplab_fontweight)
						ax.get_yticklabels()[ix].set_fontsize(grouplab_size)
				except AttributeError:
					pass

	return ax


def despineplot(despine: bool, ax: Axes) -> Axes:
	"""
	Despine the plot by removing the top, left, and right borders.

	Parameters
	----------
	despine (bool)
		If True, despine.
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------	
		Matplotlib Axes object.		
	"""
	if despine:
		ax.spines["top"].set_color("None")
		ax.spines["left"].set_color("None")
		ax.spines["right"].set_color("None")
	return ax


def format_tableheader(
	annoteheaders: Union[list, tuple],
	right_annoteheaders: Union[list, tuple],
	ax: Axes,
	**kwargs
) -> Axes:
	"""
	Format the tableheader as the first row in the data.

	Parameters
	----------
	annoteheaders (list-like)
		List of table headers to use as column headers for the additional annotations
		on the left-hand side of the plot.
	right_annoteheaders (list-like)
		List of table headers to use as column headers for the additional annotations
		on the right-hand side of the plot.
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------
		Matplotlib Axes object.
	"""
	if (annoteheaders is not None) or (right_annoteheaders is not None):
		tableheader_fontweight = kwargs.get("tableheader_fontweight", "bold")
		tableheader_fontsize = kwargs.get("tableheader_fontsize", 10)

		nlast = len(ax.get_yticklabels())  # last row is table header
		ax.get_yticklabels()[nlast - 1].set_fontweight(tableheader_fontweight)
		ax.get_yticklabels()[nlast - 1].set_fontsize(tableheader_fontsize)

	return ax


def format_xlabel(xlabel: str, ax: Axes, **kwargs) -> Axes:
	"""
	Format the x-axis label

	Parameters
	----------
	xlabel (str)
		Title of the left-hand side x-axis.
	ax (Matplotlib Axes)
		Axes to operate on.
		
	Returns
	-------
		Matplotlib Axes object.
	"""
	if xlabel is not None:
		# Retrieve settings from kwargs
		xlabel_size = kwargs.get("xlabel_size", 10)
		xlabel_fontweight = kwargs.get("xlabel_fontweight", "bold")
		ax.set_xlabel(xlabel, size=xlabel_size, fontweight=xlabel_fontweight)
	return ax


def format_xticks(
	dataframe: pd.core.frame.DataFrame,
	ll: str,
	hl: str,
	xticks: Union[tuple, list],
	ax: Axes,
	**kwargs
) -> Axes:
	"""
	Format the xtick labels.

	This function sets the range of the x-axis using the lowest value and highest values 
	in the confidence interval.
	Sets the xticks according to the user-provided 'xticks' or just use 5 tickers.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	ll (str)
		Name of column containing the lower limit of the confidence intervals. 
		Optional
	hl (str)
		Name of column containing the upper limit of the confidence intervals. 
		Optional		
	xticks (list-like)
		List of xtickers to print on the x-axis.
	ax (Matplotlib Axes)
		Axes to operate on.
		
	Returns
	-------
		Matplotlib Axes object.	
	"""
	nticks = kwargs.get("nticks", 5)
	xtick_size = kwargs.get("xtick_size", 9)

	xlowerlimit = dataframe[ll].min()
	xupperlimit = dataframe[hl].max()

	ax.set_xlim(xlowerlimit, xupperlimit)
	if xticks is not None:
		ax.set_xticklabels(xticks, fontsize=xtick_size)
	else:
		ax.xaxis.set_major_locator(plt.MaxNLocator(nticks))

	ax.tick_params(axis="x", labelsize=xtick_size)

	return ax


def draw_xticks(xticks: Union[list, tuple], ax: Axes, **kwargs):
	"""
	Draws the xtick labels if 'xticks' is specified.

	Parameters
	----------
	xticks (list-like)
		List of xtickers to print on the x-axis.
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------
		Matplotlib Axes object.
	"""
	xtick_size = kwargs.get("xtick_size", 9)

	if xticks is not None:
		ax.set_xticklabels(xticks, fontsize=xtick_size)
	else:
		ax.tick_params(axis="x", labelsize=xtick_size)

	return ax


def draw_alt_row_colors(
	dataframe: pd.core.frame.DataFrame,
	groupvar: str,
	annoteheaders: Union[list, tuple],
	right_annoteheaders: Union[list, tuple],
	ax: Axes,
	**kwargs
):
	"""
	Color alternating rows in the plot.

	Colors the even-numbered rows gray unless they are rows that indicate groups.
	Breaks from groups will restart with gray.

	Parameters
	----------
	dataframe (pandas.core.frame.DataFrame)
		Pandas DataFrame where rows are variables. Columns are variable name, estimates,
		margin of error, etc.
	groupvar (str)
		Name of column containing group of variables.
	annoteheaders (list-like)
		List of table headers to use as column headers for the additional annotations
		on the left-hand side of the plot.
	right_annoteheaders (list-like)
		List of table headers to use as column headers for the additional annotations
		on the right-hand side of the plot.
	ax (Matplotlib Axes)
		Axes to operate on.

	Returns
	-------
		Matplotlib Axes object.		
	"""
	# Retrieve settings
	row_color = kwargs.get("row_color", "black")

	if (annoteheaders is not None) or (right_annoteheaders is not None):
		headers_exist = True
	else:
		headers_exist = False

	yticklabels = ax.get_yticklabels()
	counter = 1
	if groupvar is not None:
		groups = [
			grp_str.strip().lower()
			for grp_str in dataframe[groupvar].unique()
			if isinstance(grp_str, str)
		]
	else:
		groups = []

	for ix, ticklab in enumerate(yticklabels):
		if headers_exist and (ix == len(yticklabels) - 1):
			break
		labtext = ticklab.get_text()
		if labtext.lower().strip() in groups:
			counter = 2  # reset
		else:  # color if even row
			if counter % 2 == 0:
				ax.axhspan(ix - 0.5, ix + 0.5, color=row_color, alpha=0.08, zorder=0)
			counter += 1

	return ax
