# Auxiliaries for jupyosys notebook
#
# (c) 2020 <hackfin@section5.ch>
#
import graphviz
import os
import subprocess
from myhdl import *
# from io import StringIO
from lfsr8 import lfsr8

def design_from_entity(ent, async_reset = False):
	clk = Signal(bool())
	debug = Signal(bool(0))
	ce = Signal(bool())
	reset = ResetSignal(0, 1, isasync = async_reset)
	dout = Signal(intbv()[8:])
	a = ent(clk, ce, reset, dout, debug)
	name = ent.func.__name__

	design = yshelper.Design(name)

	# a.convert("verilog")
	a.convert("yosys_module", design, name=name, trace=True)

	return design

def setupCosimulation(name, use_assert, interface):
	# logger = StringIO()
	tb = "tb_" + name
	objfile = "%s.o" % name
	if os.path.exists(objfile):
		os.remove(objfile)
	analyze_cmd = ['iverilog', '-g2012']
	analyze_cmd += ['-o', objfile, '%s.v' % name, '%s.v' % tb]
	if use_assert:
		analyze_cmd += ['../../myhdl/test/conversion/toYosys/aux/assert.v']
	subprocess.call(analyze_cmd)
	simulate_cmd = ['vvp', '-m', '../../cosimulation/icarus/myhdl.vpi']
	simulate_cmd += [ objfile ]
	c = Cosimulation(simulate_cmd, **interface)
	c.name = name
	return c

@block
def clkgen(clk, DELAY):
	@always(delay(DELAY))
	def clkgen():
		clk.next = not clk

	return instances()

@block
def tb_unit(uut, uut_syn, async_reset):
	clk = Signal(bool())
	debug, debug_syn = [ Signal(bool(0)) for i in range(2) ]
	ce = Signal(bool())
	dout, do_syn = [ Signal(intbv()[8:]) for i in range(2) ]
	reset = ResetSignal(0, 1, isasync = async_reset)

	inst_clkgen = clkgen(clk, 1)
	inst_uut = uut(clk, ce, reset, dout, debug)
	inst_syn = uut_syn(uut, clk, ce, reset, do_syn, debug_syn)

	r0 = Signal(modbv()[8:])

	inst_lfsr0 = lfsr8(clk, 1, reset, 0, r0)

	@always_comb
	def assign():
		ce.next = r0[0]

	@instance
	def stimulus():
		# errcount = 0
		reset.next = 1
		yield(delay(200))
		reset.next = 0
		while 1:
			yield clk.posedge
			print(dout, debug, " --- ", do_syn, debug_syn)
			if dout != do_syn or debug != debug_syn:
				yield clk.posedge
				yield clk.posedge
				yield clk.posedge
				raise ValueError("Simulation mismatch")

	return instances()


@block
def mapped_uut_assert(which, clk, ce, reset, dout, debug):
	args = locals()
	name = which.func.__name__ + "_mapped"
	del args['which']

	return setupCosimulation(name, True, args)


def to_svg(design, which = ""):
	print("Generating RTL image...")
	design.display_rtl(which, fmt="dot")

	f = open(design.name + ".dot")
	dot_graph = f.read()


	return graphviz.Source(dot_graph)
