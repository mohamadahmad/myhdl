# Simple entity tests for toYosys conversion
#
import myhdl
from myhdl import *
from .cosim_common import *
from .lfsr8 import lfsr8
import pytest

@block
def up_counter(clk, ce, reset, counter):
	"Counter with implicit register inference"

	@always_seq(clk.posedge, reset)
	def worker():
		if ce:
			counter.next = counter + 1

	return instances()

@block
def up_counter_reg(clk, ce, reset, counter):
	"Counter with explicit register instance"
	c = Signal(intbv(0)[len(counter):0])

	@always_seq(clk.posedge, reset)
	def worker():
		if ce:
			c.next = c + 1

	@always_comb
	def assign():
		counter.next = c

	return instances()


@block
def simple_expr(clk, ce, reset, dout, debug):
	"Simple static expressions"
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def assign():
		if counter % 4 == 0:
			dout.next = 1 | 4 | 2
		else:
			dout.next = 0

	return instances()


@block
def bool_ops(clk, ce, reset, dout, debug):
	"Simple static expressions"
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	b0, b1, b2 = [ Signal(bool()) for i in range(3) ]

	@always_comb
	def assign():
		b0.next = counter < 4 or counter == 8 or counter > 22
		b1.next = counter > 4 and counter < 8 and counter != 6
		b2.next = ounter > 2 and counter < 12 or counter == 8

	
	@always_comb
	def assign():
		debug.next = b0 ^ b1 ^ b2

	return instances()


@block
def if_expr(clk, ce, reset, dout, debug):
	"IfExpr"
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def assign():
		debug.next = 0
		dout.next = 3 if counter == 5 else 9

	return instances()

@block
def simple_reset_expr(clk, ce, reset, dout, debug):
	"Simple static expressions"
	q = Signal(modbv(0)[8:])
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_seq(clk.posedge, reset)
	def worker():
		q.next = counter

	@always_comb
	def assign():
		dout.next = q

	return instances()

@block
def simple_reset_expr(clk, ce, reset, dout, debug):
	"Simple static expressions"
	q = Signal(modbv(0)[8:])
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_seq(clk.posedge, reset)
	def worker():
		q.next = counter

	@always_comb
	def assign():
		dout.next = q

	return instances()

@block
def proc_expr(clk, ce, reset, dout, debug):
	"Simple procedural expressions inside concurrent process, 'for' loops"
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def assign():
		tmp = intbv(0xaa)[8:]
		for i in range(4):
			tmp[i*2] = counter[i]
			tmp[i*2+1] = counter[i+4]
		dout.next = tmp

	return instances()

@block
def assign_slice_legacy(clk, ce, reset, dout, debug):
	"Legacy style element assignment"
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def assign():
		dout.next[0] = counter[0]

	return instances()

@block
def assign_slice_new(clk, ce, reset, dout, debug):
	"New 'nice' way of assigning a slice next"
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def assign():
		b = counter
		dout[0].next = b[0]

	return instances()


@block
def process_variables(clk, ce, reset, dout, debug):
	"Usage of variables inside process"
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def assign():
		rmod = counter % 4
		if rmod == 0:
			dout.next = 1 | 4 | 2
		else:
			dout.next = 0

	return instances()

@block
def simple_variable(clk, ce, reset, dout, debug):
	"Simple variable example"
	counter = Signal(modbv(0)[8:])
	cr = ResetSignal(0, 1, isasync = False)
	ctr = up_counter(clk, 1, cr, counter)

	@always_seq(clk.posedge, reset)
	def fsm():		  
		v = intbv(0xff)[8:] # default value

		if ce:
			v = intbv(0xaa)[8:]
	
		dout.next = v
	@always_comb
	def assign():
		debug.next = 0
		cr.next = reset

	return instances()


@block
def module_variables(clk, ce, reset, dout, debug):
	"Module wide variables"
	counter = Signal(modbv(0)[8:])

	a = 144

	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def assign():
		rmod = counter % 4
		if rmod == 0:
			dout.next = a | 4 | 2
		else:
			dout.next = 0

	return instances()


@block
def simple_arith(clk, ce, reset, dout, debug):
	"Simple arithmetics test"
	counter = Signal(modbv(0)[8:])

	case = Signal(modbv()[8:])

	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def modulo():
		case.next = counter % 8

	@always_comb
	def select():

		if counter > 80:
			if case == 0:
				dout.next = counter % 5
			elif case == 1:
				dout.next = counter[4:] * 2
			elif case == 2:
				dout.next = counter // 2
			else:
				dout.next = counter - 1

		else:
			dout.next = 0

	return instances()

@block
def simple_cases(clk, ce, reset, dout, debug):
	"A few simple cases, to be extended"
	counter = Signal(modbv(0)[8:])

	ctr = up_counter(clk, ce, reset, counter)
	
	@always_comb
	def select():
		debug.next = counter[4]

		if counter == 14:
			dout.next = (counter & 0xf0) ^ 16 + 1
		elif counter == 15:
			dout.next = 18 // 3 # Integer division
		elif counter >= 25:
			dout.next = counter[3:] | 8
		elif counter == 26:
			dout.next = 1 | 2 | 8
		elif counter < 22:
			dout.next = (counter & 3) | 4
		else:
			dout.next = 0


	return instances()


@block
def simple_resize_cases(clk, ce, reset, dout, debug):
	counter = Signal(modbv(0)[8:])
	
	ctr = up_counter(clk, ce, reset, counter)

	@always_comb
	def select():
		debug.next = counter[4]

		if counter == 14:
			dout.next = counter[2:] | 16
		elif counter >= 25:
			dout.next = counter[4:2] | 8
		elif counter < 22:
			dout.next = counter[3:1] | 4
		else:
			dout.next = 0

	return instances()


@block
def counter_extended(clk, ce, reset, dout, debug):
	"Extended counter example"
	counter = Signal(modbv(0)[8:])
	x = Signal(modbv()[4:])
	y = Signal(modbv()[4:])

	d = Signal(intbv(3)[2:])
	
	@always_seq(clk.posedge, reset)
	def worker():
		if ce:
			debug.next = counter[4]
			counter.next = counter + 1
			d.next = 2
		else:
			d.next = 1
			debug.next = 0
			counter.next = counter

	@always_comb
	def select():
		if counter == 14:
			x.next = d + 1
			y.next = 2
		elif counter >= 118:
			x.next = (d - 1)
			y.next = 4
		elif counter < 22:
			x.next = 2
			y.next = 0
		else:
			if ce:
				x.next = 8
				y.next = 3
			else:
				x.next = 1
				y.next = 1

	@always_comb
	def assign():
		dout.next = x ^ y

	return instances()


@block
def lfsr8_0(clk, ce, reset, dout, debug):
	"""LFSR with all states"""
	x = Signal(modbv(0)[8:])
	f = Signal(bool())

	@always_seq(clk.posedge, reset)
	def worker():
		if ce == 1:
			x.next = concat(x[6], x[5], x[4], x[3] ^ f, x[2] ^ f, x[1] ^ f, x[0], f)

	@always_comb
	def assign():
		e = x[7:0] == 0
		f.next = x[7] ^ e
		dout.next = x

	return instances()

@block
def lfsr8_1(clk, ce, reset, dout, debug):
	"""LFSR with all states"""

	a, b = [ Signal(modbv()[8:]) for i in range(2) ]

	inst_lfsr = lfsr8(clk, ce, reset, 0, a)

	@always_comb
	def assign():
		dout.next = a

	return instances()


@block
def simple_logic_unused_pin(clk, a_in, b_in, y_out):
	@always_comb
	def worker():
		y_out.next = a_in ^ b_in

	return instances()

@block
def unused_pin(clk, ce, reset, dout, debug):
	a, b = [ Signal(intbv()[8:]) for i in range(2) ]

	inst_lfsr1 = lfsr8(clk, ce, reset, 0, a)
	inst_lfsr2 = lfsr8(clk, ce, reset, 4, b)

	uut = simple_logic_unused_pin(None, a, b, dout)

	return instances()

@block
def simple_sr(clk, ce, reset, dout, debug):
	"Simple parametric shift register"
	counter = Signal(modbv(0)[8:])
	cr = ResetSignal(0, 1, isasync = False)

	ctr = up_counter(clk, ce, cr, counter)
	PIPE_RESET_BRANCH = 0b0001
	PIPELEN = 4
	pipe_valid = Signal(modbv(0)[PIPELEN:])

	@always_seq(clk.posedge, reset)
	def worker():
		ibranch = counter[5]
		preset = counter[7]

		if preset == 1:
			pipe_valid.next = 0b0010
		elif ibranch == 1:
			pipe_valid.next = PIPE_RESET_BRANCH
		else:
			pipe_valid.next = concat(pipe_valid[PIPELEN-1:], ce)


	@always_comb
	def assign():
		dout.next = pipe_valid
		cr.next = reset

	return instances()

@block
def simple_shift_right(clk, ce, reset, dout, debug):
	"Arithmetic shift right"
	counter = Signal(modbv(0)[8:])
	cr = ResetSignal(0, 1, isasync = False)
	ctr = up_counter(clk, ce, cr, counter)

	@always(clk.posedge)
	def worker():
		index = counter[2:]

		if ce:
			dout.next = counter[8:2] >> index
		else:
			dout.next = counter[8:2].signed() >> index

		debug.next = True

	@always_comb
	def assign():
		cr.next = reset

	return instances()

@block
def concat_const(clk, ce, reset, dout, debug):
	"Concat with constant string vector"
	counter = Signal(modbv(0)[8:])
	cr = ResetSignal(0, 1, isasync = False)
	ctr = up_counter(clk, ce, cr, counter)

	@always_comb
	def assign():
		dout.next = concat(counter[4:1], "00100")
		cr.next = reset
		debug.next = False

	return instances()

@block
def dynamic_slice(clk, ce, reset, dout, debug):
	"Dynamic slicer example. Infers an external $dynslice blackbox"
	counter = Signal(modbv(0)[8:])
	cr = ResetSignal(0, 1, isasync = False)

	ctr = up_counter(clk, ce, cr, counter)
	PIPE_RESET_BRANCH = 0b0001
	PIPELEN = 4

	@always(clk.posedge)
	def worker():
		index = counter[4:]
		select = counter[8:4]

		debug.next = select[int(index)]

	@always_comb
	def assign():
		dout.next = 0
		cr.next = reset

	return instances()



############################################################################
# Tests


UUT_LIST = [ simple_expr, bool_ops, simple_reset_expr, proc_expr, process_variables, simple_variable,
	module_variables, simple_arith, simple_cases, simple_resize_cases, lfsr8_1, counter_extended]

UUT_LIST += [ unused_pin, ]

UUT_LIST += [ simple_sr, simple_shift_right, concat_const ]

UUT_UNRESOLVED_LIST = [ dynamic_slice, if_expr, assign_slice_legacy, assign_slice_new ]

@pytest.mark.parametrize("uut", UUT_LIST)
def test_mapped_uut(uut):
	arst = False
	run_conversion(uut, arst, None, False) # No wrapper, no display
	run_tb(tb_unit(uut, mapped_uut, arst), 20000)

@pytest.mark.xfail
@pytest.mark.parametrize("uut", UUT_UNRESOLVED_LIST)
def test_unresolved(uut):
	arst = False
	run_conversion(uut, arst, None, True) # No wrapper, display
	run_tb(tb_unit(uut, mapped_uut, arst), 20000)


if __name__ == '__main__':
	test_unit()

