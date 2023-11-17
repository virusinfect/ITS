<?php 
session_start();
include('../assets/config.php');
error_reporting(0);
if (strlen($_SESSION['helpdesk']) == 0) {
	header('location:index.php');
}

// fetch ticket data from DB
$tid = intval($_GET['id']);

$query=mysqli_query($conn, "SELECT company.id AS company_id, company.name AS company_name, clients.id AS client_id, clients.f_name AS client_f_name, clients.l_name AS client_l_name, clients.email AS client_email, clients.telephone AS client_telephone, technicians.tech_id AS tech_id, technicians.first_name AS tech_first_name, technicians.last_name AS tech_last_name, technicians.signature AS tech_sign, tickets.equipment AS equipment, tickets.serial_no AS serial_no, tickets.fault AS fault, tickets.accessories AS accessories, tickets.notes AS notes, tickets.bench_status AS bench_status, tickets.created AS created, tickets.updated AS updated, tickets.brought_by AS brought_by, tickets.reg_sign AS reg_sign, tickets.ticket_id AS ticket_id FROM tickets LEFT JOIN company on tickets.company_id=company.id LEFT JOIN clients ON tickets.client_id=clients.id LEFT JOIN technicians ON tickets.tech_id=technicians.tech_id WHERE tickets.is_active = 1 AND ticket_id='$tid'");
$row=mysqli_fetch_array($query);

$createdTimestamp = $row['created'];
$updatedTimestamp = $row['updated'];
// convert the timestamp to a user-friendly format
$dateCreated = date("d/m/Y H:m", strtotime($createdTimestamp)); // This will display the date in the format "MM/DD/YYYY"
?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Ticket Print | ITS</title>

	<!-- Favicon -->
	<link rel="icon" type="image/x-icon" href="../dist/img/favicon.ico">
	<!-- Google Font: Source Sans Pro -->
	<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,400i,700&display=fallback">
	<!-- Font Awesome Icons -->
	<link rel="stylesheet" href="../plugins/fontawesome-free-6.1.2-web/css/all.min.css">
	<!-- Theme style -->
	<link rel="stylesheet" href="../dist/css/style.css">
</head>
<body class="layout-fixed">
	<div class="wrapper">
		<!-- Main content -->
		<section class="invoice">
			<!-- title row -->
			<div class="row">
				<div class="col-12">
					<!-- Main content -->
					<div class="invoice p-3 mb-3">
						<!-- title row -->
						<div class="row p-4">
							<div class="col-md">
								<div class="d-flex justify-content-center mb-2">
									<img  src="../dist/img/itl_logo.png" height="125px" width="125px">
								</div>
								<div class="d-flex justify-content-center">
									<h2>INTELLITECH LTD.</h2>
								</div>
								<div class="d-flex justify-content-center">
									<h4>TICKET - ITL/TN/<span class="text-danger"><?php echo htmlentities($row['ticket_id']); ?></span></h4>
								</div>
							</div><!-- ./col -->

						</div><!-- ./row -->

						<div class="row">
							<div class="col-md-10 offset-1">
								<table id="" class="table table-bordered">
									<tbody>
										<tr>
											<th colspan="1" class="text-lg">Ticket No.:</th>
											<td colspan="1" class="text-lg">ITL/TN/<?php echo htmlentities($row['ticket_id']); ?></td>
											<th colspan="1" class="text-lg">Date/Time:</th>
											<td colspan="1" class="text-lg"><?php echo htmlentities($dateCreated); ?></td>
										</tr>
										<tr>
											<th colspan="1" class="text-lg">Client:</th>
											<td colspan="" class="text-lg"><?php echo htmlentities($row['company_name']); ?></td>
											<th colspan="1" class="text-lg">User:</th>
											<td colspan="" class="text-lg"><?php echo htmlentities($row['client_f_name'].' '.$row['client_l_name']); ?></td>
										</tr>
										<tr>
											<th class="text-lg">Email:</th>
											<td class="text-lg"><?php echo htmlentities($row['client_email']); ?></td>
											<th class="text-lg">Telephone:</th>
											<td class="text-lg"><?php echo htmlentities($row['client_telephone']); ?></td>
										</tr>
										<tr>
											<th class="text-lg">Equipment:</th>
											<td class="text-lg"><?php echo htmlentities($row['equipment']); ?></td>
											<th class="text-lg">Serial No.:</th>
											<td class="text-lg"><?php echo htmlentities($row['serial_no']); ?></td>
										</tr>
										<tr>
											<th colspan="1" class="text-lg">Reported Fault:</th>
											<td colspan="3" class="text-lg"><?php echo htmlentities($row['fault']); ?></td>
										</tr>
										<?php if (!empty($row['accessories'])): ?>
											<tr>
												<th colspan="1" class="text-lg">Accessories</th>
												<td colspan="3" class="text-lg"><?php echo htmlentities($row['accessories']); ?></td>
											</tr>
										<?php endif ?>

									</tbody>
								</table>
							</div>
							<!-- ./col -->
						</div>
						<!-- ./row -->

						<div class="row">
							<!-- accepted payments column -->
							<div class="col-md-10 offset-1">
								<p class="text-justify text-md">Please be advised that <strong><i>Intellitech Ltd. </i></strong><i>accepts all equipment on a best-effort basis. Please note that there may be delays in resolving problems if certain spares and/or workshop manuals are not available. Furthermore, we cannot guarantee to solve any specific problem and reserve the right to charge for parts and labor even if the issue remains unresolved. By signing below, you acknowledge and agree to these terms and conditions.</i></p>
							</div>
							<!-- /.col -->
						</div>
						<!-- /.row -->

						<div class="row">
							<div class="col-md-10 offset-1">
								<table id="" class="table table-bordered mb-3">
									<tbody>
										<tr>
											<th>Customer:</th>
											<td><?php echo htmlentities($row['brought_by']); ?></td>
											<th>Technician:</th>
											<td><?php echo htmlentities($row['tech_first_name'] . ' ' . $row['tech_last_name']); ?></td>
										</tr>
										<tr>
											<th class="text-md">Customer's Signature:</th>
											<td><img src="<?php echo htmlentities($row['reg_sign']); ?>" oncontextmenu="return false;" width="200px" height="100px"></td>
											<th class="text-md">Technician's Signature:</th>
											<td><img src="<?php echo htmlentities($row['tech_sign']); ?>" oncontextmenu="return false;" width="200px" height="100px"></td>
										</tr>
									</tbody>
								</table>
							</div>
							<!-- ./col -->
						</div>
						<!-- ./row -->


						<div class="row">
							<!-- accepted payments column -->
							<div class="col-md-10 offset-1">
								<p class="text-sm">ITL/TN/<?php echo htmlentities($row['ticket_id']); ?></p>
								<?php 

								$hid=$_SESSION['helpdesk'];
								$query=mysqli_query($conn,"SELECT name FROM helpdesk WHERE id='$hid'");
								while($fetch=mysqli_fetch_array($query)) {
									?>
									<p class="text-sm">Served by <i><?php echo htmlentities($fetch['name']); ?></i> | ITS &#8482;</p>
								<?php } ?>
							</div>
							<!-- /.col -->
						</div>
						<!-- /.row -->

						<!-- letter-footer -->
						<div class="d-flex justify-content-center fixed-bottom">
							<img  src="../dist/img/tr_footer.png" width="100%" height="100%">
						</div>
						<!-- /.letter-footer -->

					</div>
					<!-- /.invoice -->
				</div><!-- /.col -->
			</div><!-- /.row -->
		</section>
		<!-- /.content -->
	</div>
	<!-- ./wrapper -->
	<!-- Page specific script -->
	<script>
		window.addEventListener("load", window.print());
	</script>
</body>
</html>